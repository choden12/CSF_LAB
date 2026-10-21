"""Q1: Rod cutting."""

from time import perf_counter


def price_table(n):
    prices = [0, 1, 5, 8, 9, 10, 17, 17, 20, 24, 30]
    prices.extend(3 * i for i in range(11, n + 1))
    return prices


def reconstruct(first, n):
    pieces = []
    while n:
        pieces.append(first[n])
        n -= first[n]
    return pieces


def rod_naive(prices, n):
    calls = 0
    first = [0] * (n + 1)

    def solve(length):
        nonlocal calls
        calls += 1
        if length == 0:
            return 0
        best = -float('inf')
        for cut in range(1, length + 1):
            revenue = prices[cut] + solve(length - cut)
            if revenue > best:
                best = revenue
                first[length] = cut
        return best

    revenue = solve(n)
    return revenue, reconstruct(first, n), calls


def rod_memoized(prices, n):
    calls = 0
    memo = [None] * (n + 1)
    memo[0] = 0
    first = [0] * (n + 1)

    def solve(length):
        nonlocal calls
        calls += 1  # Includes calls that return cached values.
        if memo[length] is not None:
            return memo[length]
        best = -float('inf')
        for cut in range(1, length + 1):
            revenue = prices[cut] + solve(length - cut)
            if revenue > best:
                best = revenue
                first[length] = cut
        memo[length] = best
        return best

    revenue = solve(n)
    return revenue, reconstruct(first, n), calls


def rod_bottom_up(prices, n):
    revenues = [0] * (n + 1)
    first = [0] * (n + 1)
    for length in range(1, n + 1):
        best = -float('inf')
        for cut in range(1, length + 1):
            candidate = prices[cut] + revenues[length - cut]
            if candidate > best:
                best = candidate
                first[length] = cut
        revenues[length] = best
    return revenues[n], reconstruct(first, n), 0


def main():
    prices = price_table(25)
    print(f'{"n":>3} {"Revenue":>8} Pieces')
    for n in range(1, 11):
        results = [method(prices, n) for method in
                   [rod_naive, rod_memoized, rod_bottom_up]]
        assert len({result[0] for result in results}) == 1
        print(f'{n:3} {results[2][0]:8} {results[2][1]}')
    print(f'\n{"n":>3} {"Version":12} {"Recursive calls":>16} {"Seconds":>12} {"Revenue":>8}')
    for n in [5, 10, 15, 20, 25]:
        for name, method in [('Naive', rod_naive), ('Memoized', rod_memoized),
                             ('Bottom-up', rod_bottom_up)]:
            start = perf_counter()
            revenue, pieces, calls = method(prices, n)
            elapsed = perf_counter() - start
            print(f'{n:3} {name:12} {calls:16} {elapsed:12.6f} {revenue:8}', flush=True)
    print('''
Naive recursion repeats subproblems: C(0)=1 and C(n)=1+sum(C(j), j=0..n-1),
so C(n)=2^n and execution time is exponential.
Memoization solves each positive length once. Counting cache-hit calls too,
there are 1+n(n+1)/2 calls and Theta(n^2) work.
Bottom-up uses no recursive calls, computes n positive-length states, and
tests n(n+1)/2 cuts. Its running time is Theta(n^2).
''')


if __name__ == '__main__':
    main()
