"""Q2: Matrix chain multiplication."""

import random


def matrix_chain(dimensions):
    n = len(dimensions) - 1
    cost = [[0] * n for _ in range(n)]
    split = [[0] * n for _ in range(n)]
    for length in range(2, n + 1):
        for i in range(n - length + 1):
            j = i + length - 1
            cost[i][j] = float('inf')
            for k in range(i, j):
                candidate = (cost[i][k] + cost[k + 1][j]
                             + dimensions[i] * dimensions[k + 1] * dimensions[j + 1])
                if candidate < cost[i][j]:
                    cost[i][j] = candidate
                    split[i][j] = k

    def parenthesize(i, j):
        if i == j:
            return f'A{i + 1}'
        k = split[i][j]
        return f'({parenthesize(i, k)}{parenthesize(k + 1, j)})'

    return cost[0][n - 1], parenthesize(0, n - 1)


def brute_chain(dimensions):
    # Try every split recursively, without memoization.
    def solve(i, j):
        if i == j:
            return 0
        return min(solve(i, k) + solve(k + 1, j)
                   + dimensions[i] * dimensions[k + 1] * dimensions[j + 1]
                   for k in range(i, j))
    return solve(0, len(dimensions) - 2)


def left_to_right_cost(dimensions):
    return sum(dimensions[0] * dimensions[i] * dimensions[i + 1]
               for i in range(1, len(dimensions) - 1))


def main():
    rng = random.Random(6)
    chains = [[30, 35, 15, 5, 10, 20, 25], [5, 4, 6, 2, 7]]
    chains += [[rng.randint(2, 40) for _ in range(n + 1)]
               for n in [2, 4, 6, 7, 8]]
    print(f'{"Dimensions":38} {"Left-to-right":>14} {"Optimal":>10} {"Brute":>10} Parenthesisation')
    for dimensions in chains:
        optimal, order = matrix_chain(dimensions)
        brute = brute_chain(dimensions)
        assert optimal == brute
        print(f'{str(dimensions):38} {left_to_right_cost(dimensions):14} {optimal:10} {brute:10} {order}')
    assert matrix_chain(chains[0])[0] == 15125
    print('All seven chains agree with brute-force search (at most 8 matrices).')


if __name__ == '__main__':
    main()
