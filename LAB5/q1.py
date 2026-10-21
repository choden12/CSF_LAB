"""Q1: Quicksort variants, comparison counts, and execution times."""

import random
from time import perf_counter


def quicksort(values, variant):
    comparisons = 0

    def less(a, b):
        nonlocal comparisons
        comparisons += 1
        return a < b

    def lomuto(lo, hi):
        if variant == 'randomised':
            p = random.randrange(lo, hi + 1)
            values[p], values[hi] = values[hi], values[p]
        pivot = values[hi]
        i = lo
        for j in range(lo, hi):
            # a <= pivot is equivalent to not (pivot < a).
            if not less(pivot, values[j]):
                values[i], values[j] = values[j], values[i]
                i += 1
        values[i], values[hi] = values[hi], values[i]
        return i

    def hoare(lo, hi):
        pivot = values[(lo + hi) // 2]
        i, j = lo - 1, hi + 1
        while True:
            i += 1
            while less(values[i], pivot):
                i += 1
            j -= 1
            while less(pivot, values[j]):
                j -= 1
            if i >= j:
                return j
            values[i], values[j] = values[j], values[i]

    def three_way(lo, hi):
        pivot = values[hi]
        lt, i, gt = lo, lo, hi
        while i <= gt:
            if less(values[i], pivot):
                values[lt], values[i] = values[i], values[lt]
                lt += 1
                i += 1
            elif less(pivot, values[i]):
                values[i], values[gt] = values[gt], values[i]
                gt -= 1
            else:
                i += 1
        return lt, gt

    def sort(lo, hi):
        while lo < hi:
            if variant == 'hoare':
                p = hoare(lo, hi)
                left_end, right_start = p, p + 1
            elif variant == 'three-way':
                lt, gt = three_way(lo, hi)
                left_end, right_start = lt - 1, gt + 1
            else:
                p = lomuto(lo, hi)
                left_end, right_start = p - 1, p + 1
            # Recurse only on the smaller partition: O(log n) stack depth.
            if left_end - lo < hi - right_start:
                sort(lo, left_end)
                lo = right_start
            else:
                sort(right_start, hi)
                hi = left_end

    if variant not in ['lomuto', 'hoare', 'randomised', 'three-way']:
        raise ValueError('Unknown quicksort variant')
    sort(0, len(values) - 1)
    return comparisons


def main():
    random.seed(5)
    print(f'{"Input":12} {"n":>6} {"Variant":12} {"Comparisons":>14} {"Seconds":>12}')
    for n in [1000, 2000, 4000, 8000, 16000]:
        inputs = {
            'random': [random.randrange(n * 10) for _ in range(n)],
            'sorted': list(range(n)),
            'reverse': list(range(n - 1, -1, -1)),
            'duplicates': [random.randrange(10) for _ in range(n)],
        }
        for name, original in inputs.items():
            expected = sorted(original)
            for variant in ['lomuto', 'hoare', 'randomised', 'three-way']:
                values = original.copy()
                start = perf_counter()
                comparisons = quicksort(values, variant)
                elapsed = perf_counter() - start
                assert values == expected
                print(f'{name:12} {n:6} {variant:12} {comparisons:14} {elapsed:12.6f}', flush=True)
    print('''
Comparisons count only comparisons between keys, including failed scan tests.
Lomuto with the last pivot takes Theta(n^2) on sorted and reverse-sorted
distinct inputs because partitions have sizes 0 and n-1. With only ten
possible keys, equal keys repeatedly enter one partition: quadratic growth.
Randomised Lomuto has expected Theta(n log n) time on distinct keys, including
sorted inputs, but still degrades on many duplicates; worst case is Theta(n^2).
Hoare uses the middle element as pivot. Sorted and reverse-sorted inputs split
well, and equal keys are shared between partitions. These input families
typically take Theta(n log n), but adversarial pivot arrangements can be quadratic.
Three-way uses the last pivot. Sorted distinct inputs produce Theta(n^2)
behavior, and reverse-sorted distinct inputs also produce highly unbalanced
partitions. Grouping equal keys makes it effective for the ten-value inputs,
with O(n) work when the number of distinct keys is bounded by ten.
Recursing on the smaller side limits stack depth; it does not fix quadratic work.
''')


if __name__ == '__main__':
    main()
