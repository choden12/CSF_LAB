"""Q4: Randomized quickselect and Miller-Rabin primality testing."""

import math
import random
from time import perf_counter


def quickselect(values, k, rng):
    """Return the k-th smallest value (k is one-based); modifies values."""
    if not 1 <= k <= len(values):
        raise ValueError('k must be between 1 and the array length')
    target = k - 1
    lo, hi = 0, len(values) - 1
    while lo <= hi:
        pivot = values[rng.randint(lo, hi)]
        lt, i, gt = lo, lo, hi
        while i <= gt:
            if values[i] < pivot:
                values[lt], values[i] = values[i], values[lt]
                lt += 1
                i += 1
            elif values[i] > pivot:
                values[i], values[gt] = values[gt], values[i]
                gt -= 1
            else:
                i += 1
        if target < lt:
            hi = lt - 1
        elif target > gt:
            lo = gt + 1
        else:
            return values[target]


def miller_rabin(n, rounds, rng):
    if rounds < 1:
        raise ValueError('Use at least one round')
    if n in (2, 3):
        return True
    if n < 2 or n % 2 == 0:
        return False
    d, s = n - 1, 0
    while d % 2 == 0:
        d //= 2
        s += 1
    for _ in range(rounds):
        a = rng.randint(2, n - 2)
        x = pow(a, d, n)
        if x in (1, n - 1):
            continue
        for _ in range(s - 1):
            x = x * x % n
            if x == n - 1:
                break
        else:
            return False
    return True


def trial_division(n):
    if n < 2:
        return False
    if n % 2 == 0:
        return n == 2
    for divisor in range(3, math.isqrt(n) + 1, 2):
        if n % divisor == 0:
            return False
    return True


def main():
    rng = random.Random(7)
    print(f'{"n":>10} {"k":>10} {"Quickselect (s)":>18} {"Sort+index (s)":>18} {"Answer":>12}')
    for n in [10000, 100000, 250000, 500000, 1000000]:
        original = [rng.randrange(10**9) for _ in range(n)]
        k = (n + 1) // 2
        values = original.copy()
        start = perf_counter()
        selected = quickselect(values, k, rng)
        select_time = perf_counter() - start
        start = perf_counter()
        expected = sorted(original)[k - 1]
        sort_time = perf_counter() - start
        assert selected == expected
        print(f'{n:10} {k:10} {select_time:18.6f} {sort_time:18.6f} {selected:12}', flush=True)
    print('Quickselect: expected O(n), worst O(n^2); sorting: O(n log n).')
    print('Built-in sorting runs in optimized native code and can be faster in these measurements.')

    print('\nTwenty random 12-digit integers; Miller-Rabin uses 10 rounds.')
    print(f'{"Number":>14} {"MR prime?":>12} {"Trial prime?":>14} {"MR seconds":>14} {"Trial seconds":>16}')
    numbers = [rng.randrange(10**11, 10**12) for _ in range(20)]
    for n in numbers:
        start = perf_counter()
        probable = miller_rabin(n, 10, rng)
        mr_time = perf_counter() - start
        start = perf_counter()
        exact = trial_division(n)
        trial_time = perf_counter() - start
        assert probable == exact
        print(f'{n:14} {str(probable):>12} {str(exact):>14} {mr_time:14.6f} {trial_time:16.6f}')
    print('Both tests agree on all 20 numbers. Miller-Rabin True means probably prime.')
    false_primes = sum(miller_rabin(561, 1, rng) for _ in range(1000))
    print(f'\n561 with one Miller-Rabin round: "prime" {false_primes}/1000 times ({false_primes / 10:.1f}%).')
    print('561 is composite (3 * 11 * 17). Each trial samples a base uniformly from 2 through 559.')


if __name__ == '__main__':
    main()
