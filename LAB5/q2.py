"""Q2: Stable counting sort, LSD radix sort, and merge sort."""

import random
from time import perf_counter
import matplotlib.pyplot as plt


def counting_sort(values, k, key=lambda x: x):
    counts = [0] * (k + 1)
    for value in values:
        counts[key(value)] += 1
    for i in range(1, k + 1):
        counts[i] += counts[i - 1]
    output = [None] * len(values)
    # Right-to-left placement preserves the order of equal keys.
    for value in reversed(values):
        digit = key(value)
        counts[digit] -= 1
        output[counts[digit]] = value
    return output


def radix_sort(values, base=10):
    result = list(values)
    maximum = max(result, default=0)
    place = 1
    while maximum // place:
        result = counting_sort(result, base - 1,
                               key=lambda x: (x // place) % base)
        place *= base
    return result


def merge_sort(values):
    if len(values) <= 1:
        return list(values)
    mid = len(values) // 2
    left, right = merge_sort(values[:mid]), merge_sort(values[mid:])
    result = []
    i = j = 0
    while i < len(left) and j < len(right):
        if left[i] <= right[j]:
            result.append(left[i])
            i += 1
        else:
            result.append(right[j])
            j += 1
    result.extend(left[i:])
    result.extend(right[j:])
    return result


def measure(function, values, *args):
    start = perf_counter()
    result = function(values, *args)
    elapsed = perf_counter() - start
    assert result == sorted(values)
    return elapsed


def main():
    rng = random.Random(5)
    pairs = [(2, 0), (1, 1), (2, 2), (0, 3), (1, 4), (2, 5)]
    ordered = counting_sort(pairs, 2, key=lambda pair: pair[0])
    print('Stability demonstration (key, original index):')
    print('Input: ', pairs)
    print('Output:', ordered)
    assert ordered == [(0, 3), (1, 1), (1, 4), (2, 0), (2, 2), (2, 5)]
    print('Equal keys retain increasing original indices.\n')

    ks = [10, 10**3, 10**5, 10**7]
    counting_times, merge_times = [], []
    print('Counting sort: n = 100000')
    print(f'{"k":>10} {"Counting (s)":>14} {"Merge (s)":>14}')
    for k in ks:
        values = [rng.randrange(k + 1) for _ in range(100000)]
        ct = measure(counting_sort, values, k)
        mt = measure(merge_sort, values)
        counting_times.append(ct)
        merge_times.append(mt)
        print(f'{k:10} {ct:14.6f} {mt:14.6f}', flush=True)

    fig, axes = plt.subplots(1, 2, figsize=(12, 5))
    axes[0].plot(ks, counting_times, 'o-', label='Counting sort')
    axes[0].plot(ks, merge_times, 'o-', label='Merge sort')
    axes[0].set_xscale('log')
    axes[0].set_xlabel('Maximum key k (n = 100000)')
    axes[0].set_ylabel('Execution time (seconds)')
    axes[0].set_title('Counting sort versus merge sort')

    sizes = [10000, 100000, 250000, 500000, 1000000]
    times = {'Radix base 10': [], 'Radix base 256': [], 'Merge sort': []}
    print('\nRadix and merge sort: k = 1000000000')
    print(f'{"n":>10} {"Base 10 (s)":>14} {"Base 256 (s)":>14} {"Merge (s)":>14}')
    for n in sizes:
        values = [rng.randrange(10**9 + 1) for _ in range(n)]
        row = [measure(radix_sort, values, 10),
               measure(radix_sort, values, 256), measure(merge_sort, values)]
        for label, elapsed in zip(times, row):
            times[label].append(elapsed)
        print(f'{n:10} {row[0]:14.6f} {row[1]:14.6f} {row[2]:14.6f}', flush=True)
    for label, elapsed in times.items():
        axes[1].plot(sizes, elapsed, 'o-', label=label)
    axes[1].set_xlabel('Input size n (k = 1000000000)')
    axes[1].set_ylabel('Execution time (seconds)')
    axes[1].set_title('Radix sort versus merge sort')
    for axis in axes:
        axis.legend()
        axis.grid(True)
    fig.tight_layout()
    print('''
Counting sort takes Theta(n+k) time and Theta(n+k) auxiliary space. It wins
when k is small relative to n; scanning a huge count array can make it lose
when k is large, even for the same n.
Stable LSD radix sort takes Theta(d(n+B)) time for d digits and base B.
For keys up to 10^9, base 10 needs at most 10 passes and base 256 needs 4.
Fewer passes can favor base 256. Merge sort takes Theta(n log n) time.
Radix sort can win for large n and fixed-width keys, but digit extraction,
extra passes, and allocation overhead can make it lose for smaller inputs.
Actual crossover points should be read from the measured plots.
''')
    plt.show()


if __name__ == '__main__':
    main()
