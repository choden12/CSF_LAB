"""Lab 4, Part B: Matrix Modular Exponentiation."""

import random
from time import perf_counter


def validate(exponent, modulus):
    if not isinstance(exponent, int) or not isinstance(modulus, int):
        raise TypeError("Exponent and modulus must be integers")
    if exponent < 0:
        raise ValueError("Exponent must be nonnegative")
    if modulus < 1:
        raise ValueError("Modulus must be at least 1")


def square_dimension(matrix):
    d = len(matrix)
    if d == 0 or any(len(row) != d for row in matrix):
        raise ValueError("Matrix must be nonempty and square")
    if any(not isinstance(x, int) for row in matrix for x in row):
        raise TypeError("Matrix entries must be integers")
    return d


def identity_matrix(d):
    if not isinstance(d, int) or d < 1:
        raise ValueError("Dimension must be a positive integer")
    return [[int(i == j) for j in range(d)] for i in range(d)]


def _multiply(a, b, m):
    # Transposition gives contiguous row access in the innermost loop.
    columns = list(zip(*b))
    return [[sum(x * y for x, y in zip(row, col)) % m
             for col in columns] for row in a]


def matrix_multiply(a, b, m):
    validate(0, m)
    if square_dimension(a) != square_dimension(b):
        raise ValueError("Matrices must have equal dimensions")
    return _multiply(a, b, m)


def matrix_setup(a, n, m):
    validate(n, m)
    d = square_dimension(a)
    return [[x % m for x in row] for row in a], [
        [x % m for x in row] for row in identity_matrix(d)]


def matrix_pow_naive(a, n, m):
    a, result = matrix_setup(a, n, m)
    for _ in range(n):
        result = _multiply(result, a, m)
    return result


def matrix_pow_binary(a, n, m):
    a, result = matrix_setup(a, n, m)
    while n:
        if n & 1:
            result = _multiply(result, a, m)
        n >>= 1
        if n:
            a = _multiply(a, a, m)
    return result


def fibonacci_mod(n, m):
    """F(0)=0, F(1)=1; [[1,1],[1,0]]**n contains F(n) at [0][1]."""
    return matrix_pow_binary([[1, 1], [1, 0]], n, m)[0][1]


def count_walks(adjacency, k, source, target, m):
    """adjacency[i][j] is the number of directed edges from i to j."""
    d = square_dimension(adjacency)
    if any(x < 0 for row in adjacency for x in row):
        raise ValueError("Edge counts must be nonnegative")
    if not (0 <= source < d and 0 <= target < d):
        raise ValueError("Vertex index out of range")
    return matrix_pow_binary(adjacency, k, m)[source][target]


def timed(function, args):
    start = perf_counter()
    result = function(*args)
    return perf_counter() - start, result


def benchmark():
    kind = 'matrix'
    cases = [(d, 2 ** p) for d in [2, 4, 8, 16, 32] for p in range(4, 13)]
    rng = random.Random(4)
    for d, exponent in cases:
        a = [[rng.randrange(100) for _ in range(d)] for _ in range(d)]
        args = (a, exponent, 1000000007)
        naive, binary = (matrix_pow_naive, matrix_pow_binary)
        slow, expected = timed(naive, args)
        fast, actual = timed(binary, args)
        assert expected == actual
        print(f'{kind:6} d={d:2} exponent={exponent:7} naive={slow:.6f}s binary={fast:.6f}s speedup={slow / fast:.1f}x', flush=True)


def main():
    print('\nMatrix comparisons:')
    for a, n, m in [([[1, 1], [1, 0]], 10, 1000), ([[2, -1], [3, 4]], 5, 17), ([[1, 2], [3, 4]], 0, 7)]:
        print(f'A={a}, n={n}, m={m}: naive={matrix_pow_naive(a, n, m)}, binary={matrix_pow_binary(a, n, m)}')
    print('\nF(10^18) mod (10^9+7) =', fibonacci_mod(10 ** 18, 10 ** 9 + 7))
    print('Walks of 4 edges from 0 to 2:', count_walks([[0, 1, 1], [0, 0, 1], [1, 0, 0]], 4, 0, 2, 1000000007))
    benchmark()


if __name__ == "__main__":
    main()
