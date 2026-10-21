"""Q3: Dijkstra, Kruskal, and Prim."""

import heapq
from pathlib import Path
import random
from time import perf_counter


def dijkstra(vertices, edges, source):
    adjacency = [[] for _ in range(vertices)]
    for u, v, weight in edges:
        adjacency[u].append((v, weight))
    distance = [float('inf')] * vertices
    parent = [None] * vertices
    distance[source] = 0
    heap = [(0, source)]
    settled = set()
    while heap:
        cost, u = heapq.heappop(heap)
        if u in settled:
            continue
        settled.add(u)
        for v, weight in adjacency[u]:
            if v not in settled and cost + weight < distance[v]:
                distance[v] = cost + weight
                parent[v] = u
                heapq.heappush(heap, (distance[v], v))
    return distance, parent


def shortest_path(parent, source, target):
    path = []
    while target is not None:
        path.append(target)
        if target == source:
            return path[::-1]
        target = parent[target]
    return []


class UnionFind:
    def __init__(self, n):
        self.parent = list(range(n))
        self.size = [1] * n

    def find(self, u):
        while self.parent[u] != u:
            self.parent[u] = self.parent[self.parent[u]]
            u = self.parent[u]
        return u

    def union(self, u, v):
        u, v = self.find(u), self.find(v)
        if u == v:
            return False
        if self.size[u] < self.size[v]:
            u, v = v, u
        self.parent[v] = u
        self.size[u] += self.size[v]
        return True


def kruskal(vertices, edges):
    forest = UnionFind(vertices)
    tree, total = [], 0
    for u, v, weight in sorted(edges, key=lambda edge: edge[2]):
        if forest.union(u, v):
            tree.append((u, v, weight))
            total += weight
            if len(tree) == vertices - 1:
                break
    if len(tree) != vertices - 1:
        raise ValueError('Graph must be connected')
    return total, tree


def prim(vertices, edges):
    adjacency = [[] for _ in range(vertices)]
    for u, v, weight in edges:
        adjacency[u].append((weight, u, v))
        adjacency[v].append((weight, v, u))
    seen = {0}
    heap = adjacency[0].copy()
    heapq.heapify(heap)
    total, tree = 0, []
    while heap and len(seen) < vertices:
        weight, u, v = heapq.heappop(heap)
        if v in seen:
            continue
        seen.add(v)
        total += weight
        tree.append((u, v, weight))
        for edge in adjacency[v]:
            if edge[2] not in seen:
                heapq.heappush(heap, edge)
    if len(seen) != vertices:
        raise ValueError('Graph must be connected')
    return total, tree


def random_connected_graph(vertices, edge_count, rng):
    pairs = set()
    edges = []

    def add(u, v):
        u, v = min(u, v), max(u, v)
        if u == v or (u, v) in pairs:
            return
        pairs.add((u, v))
        edges.append((u, v, rng.randint(1, 10000)))

    for v in range(1, vertices):
        add(rng.randrange(v), v)
    while len(edges) < edge_count:
        add(rng.randrange(vertices), rng.randrange(vertices))
    return edges


def read_graph():
    print('Directed graph file format: first line V E; then E lines: u v weight.')
    print('Vertex labels must be integers 0 through V-1; weights must be nonnegative.')
    path = Path(input('Graph file path: ').strip().strip('"'))
    rows = [line.split() for line in path.read_text(encoding='utf-8').splitlines() if line.strip()]
    vertices, count = map(int, rows[0])
    edges = [tuple(map(int, row)) for row in rows[1:]]
    if vertices < 1 or len(edges) != count:
        raise ValueError('Invalid vertex or edge count')
    for edge in edges:
        if len(edge) != 3:
            raise ValueError('Each edge needs u, v, and weight')
        u, v, weight = edge
        if not (0 <= u < vertices and 0 <= v < vertices) or weight < 0:
            raise ValueError('Invalid vertex label or negative weight')
    return vertices, edges


def main():
    vertices, edges = read_graph()
    source = int(input('Source vertex: '))
    if not 0 <= source < vertices:
        raise ValueError('Source vertex out of range')
    distance, parent = dijkstra(vertices, edges, source)
    print(f'{"Vertex":>8} {"Distance":>12} Path')
    for v in range(vertices):
        path = shortest_path(parent, source, v)
        print(f'{v:8} {distance[v]:12} {path if path else "unreachable"}')

    rng = random.Random(7)
    for _ in range(20):
        v = rng.randint(2, 60)
        e = rng.randint(v - 1, v * (v - 1) // 2)
        graph = random_connected_graph(v, e, rng)
        assert kruskal(v, graph)[0] == prim(v, graph)[0]
    print('\nMST totals agree on 20 random connected undirected graphs.')
    print(f'{"Graph":8} {"V":>6} {"E":>9} {"Kruskal (s)":>14} {"Prim (s)":>14} {"MST weight":>14} Winner')
    for label, count in [('Sparse', 3000), ('Dense', 250000)]:
        graph = random_connected_graph(1000, count, rng)
        start = perf_counter()
        kw, kt = kruskal(1000, graph)
        kruskal_time = perf_counter() - start
        start = perf_counter()
        pw, pt = prim(1000, graph)
        prim_time = perf_counter() - start
        assert kw == pw
        winner = 'Kruskal' if kruskal_time < prim_time else 'Prim'
        print(f'{label:8} {1000:6} {count:9} {kruskal_time:14.6f} {prim_time:14.6f} {kw:14} {winner}', flush=True)
    print('''
Kruskal sorts all E edges: O(E log E). This heap-based Prim builds adjacency
lists and can push O(E) entries: O(E log E) worst-case time for this lazy heap.
On sparse graphs, both have few edges; edge sorting versus heap overhead can
decide the winner. On dense graphs, Kruskal sorts many edges, while Prim builds
large adjacency lists and may push many heap entries. The measured winner
depends on these costs and the graph; density alone does not guarantee a winner.
Both timings include each algorithm's graph preparation, excluding generation.
''')

    small = [(0, 1, 2), (0, 2, 5), (1, 3, 2)]
    print('Nonnegative example edges:', small)
    print('Dijkstra distances:', dijkstra(4, small, 0)[0])
    small.append((2, 1, -4))
    print('After adding one negative edge (2, 1, -4):', small)
    print('Dijkstra distances:', dijkstra(4, small, 0)[0])
    print('True distances: [0, 1, 5, 3]; paths to 1 and 3 go through vertex 2.')
    print('Dijkstra settles vertex 1 too early, so its greedy assumption fails.')


if __name__ == '__main__':
    main()
