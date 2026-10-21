"""Q1: Activity selection and knapsack."""

import random


def activity_selection(activities, rule='finish'):
    keys = {'finish': lambda a: (a[1], a[0]),
            'start': lambda a: (a[0], a[1]),
            'duration': lambda a: (a[1] - a[0], a[1], a[0])}
    selected = []
    for start, finish in sorted(activities, key=keys[rule]):
        if all(finish <= s or f <= start for s, f in selected):
            selected.append((start, finish))
    return sorted(selected)


def fractional_knapsack(items, capacity):
    # Items are (weight, value); returned fractions use original item indices.
    value = 0.0
    fractions = []
    for i, (weight, worth) in sorted(enumerate(items),
                                    key=lambda item: item[1][1] / item[1][0], reverse=True):
        fraction = min(1, capacity / weight)
        if fraction > 0:
            fractions.append((i, fraction))
            value += fraction * worth
            capacity -= fraction * weight
        if capacity <= 0:
            break
    return value, fractions


def greedy_zero_one(items, capacity):
    total = 0
    selected = []
    for i, (weight, value) in sorted(enumerate(items),
                                    key=lambda item: item[1][1] / item[1][0], reverse=True):
        if weight <= capacity:
            total += value
            capacity -= weight
            selected.append(i)
    return total, selected


def dp_zero_one(items, capacity):
    best = [0] * (capacity + 1)
    for weight, value in items:
        for remaining in range(capacity, weight - 1, -1):
            best[remaining] = max(best[remaining], best[remaining - weight] + value)
    return best[capacity]


def main():
    count = int(input('Number of activities: '))
    activities = []
    for i in range(count):
        while True:
            try:
                start, finish = map(int, input(
                    f'Activity {i + 1} (start finish, example: 1 4): ').split())
                if start >= finish:
                    print('Start must be less than finish. Try again.')
                    continue
                break
            except ValueError:
                print('Enter two integers separated by a space, for example: 1 4')
        activities.append((start, finish))
    print('Earliest-finish selected set:', activity_selection(activities))

    rng = random.Random(7)
    found = {}
    for trial in range(1, 100001):
        sample = []
        for _ in range(rng.randint(4, 12)):
            start = rng.randrange(20)
            sample.append((start, start + rng.randint(1, 12)))
        optimal = activity_selection(sample)
        for rule in ['start', 'duration']:
            other = activity_selection(sample, rule)
            if rule not in found and len(other) < len(optimal):
                found[rule] = (trial, sample, optimal, other)
        if len(found) == 2:
            break
    for rule in ['start', 'duration']:
        if rule not in found:
            print(f'No {rule} counterexample found in 100000 trials.')
            continue
        trial, sample, optimal, other = found[rule]
        print(f'\nCounterexample for earliest {rule}' if rule == 'start'
              else '\nCounterexample for shortest duration')
        print('Random trial:', trial, 'Input:', sample)
        print('Earliest finish:', optimal, 'Count:', len(optimal))
        print('Other rule:', other, 'Count:', len(other))

    count = int(input('\nNumber of knapsack items: '))
    items = []
    for i in range(count):
        while True:
            try:
                weight, value = map(int, input(
                    f'Item {i + 1} (weight value, example: 10 60): ').split())
                if weight <= 0 or value < 0:
                    print('Weight must be positive and value nonnegative. Try again.')
                    continue
                break
            except ValueError:
                print('Enter two integers separated by a space, for example: 10 60')
        items.append((weight, value))
    capacity = int(input('Knapsack capacity: '))
    if capacity < 0:
        raise ValueError('Capacity must be nonnegative')
    value, fractions = fractional_knapsack(items, capacity)
    print('Fractional maximum value:', value)
    print('Fractions (zero-based item index, fraction):', fractions)
    print('0/1 ratio greedy (value, selected indices):', greedy_zero_one(items, capacity))
    print('0/1 DP optimal value:', dp_zero_one(items, capacity))

    worst = 1.0
    worst_case = None
    for _ in range(10000):
        capacity = rng.randint(5, 100)
        items = [(rng.randint(1, capacity), rng.randint(1, 200))
                 for _ in range(rng.randint(2, 15))]
        greedy, selected = greedy_zero_one(items, capacity)
        optimal = dp_zero_one(items, capacity)
        ratio = greedy / optimal
        if worst_case is None or ratio < worst:
            worst = ratio
            worst_case = (items, capacity, greedy, optimal)
    print('\nWorst greedy/optimal ratio in 10000 random trials:', f'{worst:.6f}')
    print('Items (weight, value), capacity, greedy value, optimal value:', worst_case)
    print('This is an observed ratio, not a guaranteed approximation bound.')


if __name__ == '__main__':
    main()
