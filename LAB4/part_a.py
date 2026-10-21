"""Lab 4, Part A: Modular Exponentiation."""

from time import perf_counter


def validate(exponent, modulus):
    if not isinstance(exponent, int) or not isinstance(modulus, int):
        raise TypeError("Exponent and modulus must be integers")
    if exponent < 0:
        raise ValueError("Exponent must be nonnegative")
    if modulus < 1:
        raise ValueError("Modulus must be at least 1")


def mod_pow_naive(a, b, m):
    validate(b, m)
    a %= m
    result = 1 % m
    for _ in range(b):
        result = result * a % m
    return result


def mod_pow_binary(a, b, m):
    """Arithmetic square-and-multiply: O(log b) modular multiplications."""
    validate(b, m)
    a %= m
    result = 1 % m
    while b:
        if b % 2:
            result = result * a % m
        b //= 2
        if b:
            a = a * a % m
    return result


def mod_pow_bitwise(a, b, m):
    validate(b, m)
    a %= m
    result = 1 % m
    while b:
        if b & 1:
            result = result * a % m
        b >>= 1
        if b:
            a = a * a % m
    return result


def timed(function, args):
    start = perf_counter()
    result = function(*args)
    return perf_counter() - start, result


def benchmark():
    kind = 'scalar'
    cases = [(1, 10 ** p) for p in range(1, 7)]
    for d, exponent in cases:
        args = (123456789, exponent, 1000000007)
        naive, binary = (mod_pow_naive, mod_pow_bitwise)
        slow, expected = timed(naive, args)
        fast, actual = timed(binary, args)
        assert expected == actual
        print(f'{kind:6} d={d:2} exponent={exponent:7} naive={slow:.6f}s binary={fast:.6f}s speedup={slow / fast:.1f}x', flush=True)


def main():
    print('\nScalar comparisons (naive, arithmetic binary, bitwise binary):')
    for a, b, m in [(2, 10, 1000), (-3, 5, 13), (5, 0, 1), (7, 100, 101)]:
        print((a, b, m), [f(a, b, m) for f in [mod_pow_naive, mod_pow_binary, mod_pow_bitwise]])
    benchmark()


if __name__ == "__main__":
    main()
