"""Q3: Longest common subsequence and line-by-line diff."""

import random
from pathlib import Path
from time import perf_counter


def lcs_table(x, y):
    table = [[0] * (len(y) + 1) for _ in range(len(x) + 1)]
    for i in range(1, len(x) + 1):
        for j in range(1, len(y) + 1):
            if x[i - 1] == y[j - 1]:
                table[i][j] = table[i - 1][j - 1] + 1
            else:
                table[i][j] = max(table[i - 1][j], table[i][j - 1])
    return table


def reconstruct_lcs(x, y, table):
    result = []
    i, j = len(x), len(y)
    while i and j:
        if x[i - 1] == y[j - 1]:
            result.append(x[i - 1])
            i -= 1
            j -= 1
        elif table[i - 1][j] >= table[i][j - 1]:
            i -= 1
        else:
            j -= 1
    return result[::-1]


def lcs_length_two_rows(x, y):
    if len(y) > len(x):
        x, y = y, x
    previous = [0] * (len(y) + 1)
    for item in x:
        current = [0] * (len(y) + 1)
        for j, other in enumerate(y, 1):
            if item == other:
                current[j] = previous[j - 1] + 1
            else:
                current[j] = max(previous[j], current[j - 1])
        previous = current
    return previous[-1]


def brute_lcs_length(x, y):
    best = 0
    # Enumerate every one of X's 2^len(X) subsequences.
    for mask in range(1 << len(x)):
        subsequence = [x[i] for i in range(len(x)) if mask & (1 << i)]
        position = 0
        for item in y:
            if position < len(subsequence) and subsequence[position] == item:
                position += 1
        if position == len(subsequence):
            best = max(best, position)
    return best


def line_diff(old_lines, new_lines):
    table = lcs_table(old_lines, new_lines)
    result = []
    i, j = len(old_lines), len(new_lines)
    while i or j:
        if i and j and old_lines[i - 1] == new_lines[j - 1]:
            result.append((' ', old_lines[i - 1]))
            i -= 1
            j -= 1
        elif j and (not i or table[i][j - 1] > table[i - 1][j]):
            result.append(('+', new_lines[j - 1]))
            j -= 1
        else:
            result.append(('-', old_lines[i - 1]))
            i -= 1
    return result[::-1]


def main():
    x, y = 'ABCBDAB', 'BDCABA'
    table = lcs_table(x, y)
    print('LCS table: rows = X, columns = Y; - denotes the empty prefix')
    print('    ' + ' '.join(f'{c:>2}' for c in '-' + y))
    for label, row in zip('-' + x, table):
        print(f'{label:>2}  ' + ' '.join(f'{value:2}' for value in row))
    print('One LCS:', ''.join(reconstruct_lcs(x, y, table)))
    print('Two-row LCS length:', lcs_length_two_rows(x, y))
    rng = random.Random(6)
    print(f'\n{"Length":>6} {"LCS":>5} {"DP seconds":>14} {"Brute seconds":>14}')
    for n in range(5, 19):
        x = ''.join(rng.choice('ABCD') for _ in range(n))
        y = ''.join(rng.choice('ABCD') for _ in range(n))
        start = perf_counter()
        result = lcs_table(x, y)[-1][-1]
        dp_time = perf_counter() - start
        start = perf_counter()
        brute = brute_lcs_length(x, y)
        brute_time = perf_counter() - start
        assert result == brute == lcs_length_two_rows(x, y)
        print(f'{n:6} {result:5} {dp_time:14.6f} {brute_time:14.6f}', flush=True)
    print('\nLine diff: space = unchanged, - = removed, + = added.')
    while True:
        try:
            old_path = input('First text file path: ').strip().strip('"')
            old_lines = Path(old_path).read_text(encoding='utf-8').splitlines()
            new_path = input('Second text file path: ').strip().strip('"')
            new_lines = Path(new_path).read_text(encoding='utf-8').splitlines()
            break
        except (OSError, UnicodeError) as error:
            print(f'Cannot read text file: {error}. Enter the paths again.')
    for prefix, line in line_diff(old_lines, new_lines):
        print(f'{prefix} {line}')


if __name__ == '__main__':
    main()
