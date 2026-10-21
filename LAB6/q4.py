"""Q4 (Optional): Optimal binary search tree."""


def optimal_bst(p, q):
    n = len(p)
    # Keys are indexed 1..n; dummy leaves are indexed 0..n.
    p = [0] + list(p)
    expected = [[0.0] * (n + 2) for _ in range(n + 2)]
    weight = [[0.0] * (n + 2) for _ in range(n + 2)]
    root = [[0] * (n + 2) for _ in range(n + 2)]
    for i in range(1, n + 2):
        expected[i][i - 1] = q[i - 1]
        weight[i][i - 1] = q[i - 1]
    for length in range(1, n + 1):
        for i in range(1, n - length + 2):
            j = i + length - 1
            expected[i][j] = float('inf')
            weight[i][j] = weight[i][j - 1] + p[j] + q[j]
            for r in range(i, j + 1):
                cost = expected[i][r - 1] + expected[r + 1][j] + weight[i][j]
                if cost < expected[i][j]:
                    expected[i][j] = cost
                    root[i][j] = r
    return expected[1][n], root


def print_tree(root, i, j, prefix='Root', indent=''):
    if i > j:
        print(f'{indent}{prefix}: d{j} (unsuccessful search)')
        return
    r = root[i][j]
    print(f'{indent}{prefix}: k{r}')
    print_tree(root, i, r - 1, 'Left', indent + '  ')
    print_tree(root, r + 1, j, 'Right', indent + '  ')


def main():
    p = [0.15, 0.10, 0.05, 0.10, 0.20]
    q = [0.05, 0.10, 0.05, 0.05, 0.05, 0.10]
    cost, root = optimal_bst(p, q)
    assert abs(cost - 2.75) < 1e-9
    print(f'Expected search cost: {cost:.2f}')
    print_tree(root, 1, len(p))


if __name__ == '__main__':
    main()
