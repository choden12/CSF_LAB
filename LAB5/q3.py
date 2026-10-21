"""Q3: Counting inversions and Kendall tau distance."""

import random
from time import perf_counter


def brute_inversions(values, time_limit=None):
    count = checks = 0
    start = perf_counter()
    for i in range(len(values)):
        for j in range(i + 1, len(values)):
            if values[i] > values[j]:
                count += 1
            checks += 1
            if time_limit is not None and checks % 4096 == 0:
                if perf_counter() - start >= time_limit:
                    raise TimeoutError('Brute force reached the 60-second limit')
    return count


def merge_inversions(values):
    def sort(a):
        if len(a) <= 1:
            return list(a), 0
        mid = len(a) // 2
        left, lc = sort(a[:mid])
        right, rc = sort(a[mid:])
        merged = []
        i = j = 0
        count = lc + rc
        while i < len(left) and j < len(right):
            if left[i] <= right[j]:
                merged.append(left[i])
                i += 1
            else:
                merged.append(right[j])
                count += len(left) - i
                j += 1
        merged.extend(left[i:])
        merged.extend(right[j:])
        return merged, count

    return sort(values)[1]


def read_ranking(label):
    while True:
        ranking = input(f'{label}: enter 10 unique movie IDs in preference order, separated by spaces: ').split()
        if len(ranking) == 10 and len(set(ranking)) == 10:
            return ranking
        print('Enter exactly 10 different movie IDs.')


def movie_distance():
    first = read_ranking('User 1')
    while True:
        second = read_ranking('User 2')
        if set(first) == set(second):
            break
        print('Both rankings must contain the same 10 movies.')
    positions = {movie: index for index, movie in enumerate(first)}
    distance = merge_inversions([positions[movie] for movie in second])
    print('Kendall tau distance:', distance, 'out of 45 pairs')
    print('0 means identical rankings; 45 means completely reversed rankings.')


def main():
    rng = random.Random(5)
    for n in [0, 1, 10, 100, 500, 1000, 1500, 2000]:
        for _ in range(3):
            values = [rng.randrange(100) for _ in range(n)]
            assert brute_inversions(values) == merge_inversions(values)
    print('Both methods agree on random arrays up to size 2000.')
    print(f'{"n":>10} {"Brute count":>16} {"Brute seconds":>16} {"Merge count":>16} {"Merge seconds":>16}')
    use_brute = True
    for n in [1000, 2000, 4000, 10000, 100000, 1000000]:
        values = [rng.randrange(n) for _ in range(n)]
        start = perf_counter()
        fast_count = merge_inversions(values)
        fast_time = perf_counter() - start
        slow_count, slow_time = '-', 'skipped'
        if use_brute:
            start = perf_counter()
            try:
                slow_count = brute_inversions(values, time_limit=60)
                slow_time = f'{perf_counter() - start:.6f}'
                assert slow_count == fast_count
            except TimeoutError:
                slow_count = 'unfinished'
                slow_time = '>=60 (stopped)'
                use_brute = False
        print(f'{n:10} {str(slow_count):>16} {slow_time:>16} {fast_count:16} {fast_time:16.6f}', flush=True)
    print('Brute force: Theta(n^2). Merge counting: Theta(n log n).')
    movie_distance()


if __name__ == '__main__':
    main()
