"""Q2: Huffman coding of at least three text files."""

from collections import Counter
import heapq
from itertools import count
from pathlib import Path


def build_codes(text):
    frequencies = Counter(text)
    sequence = count()
    heap = [(frequency, next(sequence), char) for char, frequency in frequencies.items()]
    heapq.heapify(heap)
    if not heap:
        return {}, frequencies
    while len(heap) > 1:
        left_frequency, _, left = heapq.heappop(heap)
        right_frequency, _, right = heapq.heappop(heap)
        heapq.heappush(heap, (left_frequency + right_frequency, next(sequence), (left, right)))
    codes = {}
    stack = [(heap[0][2], '')]
    while stack:
        node, prefix = stack.pop()
        if isinstance(node, str):
            codes[node] = prefix or '0'
        else:
            left, right = node
            stack.append((right, prefix + '1'))
            stack.append((left, prefix + '0'))
    return codes, frequencies


def encode(text, codes):
    return ''.join(codes[char] for char in text)


def decode(bits, codes):
    reverse = {code: char for char, code in codes.items()}
    result, current = [], ''
    for bit in bits:
        current += bit
        if current in reverse:
            result.append(reverse[current])
            current = ''
    if current:
        raise ValueError('Incomplete encoded character')
    return ''.join(result)


def main():
    summaries = []
    for index in range(1, 4):
        while True:
            path = Path(input(f'Text file {index} path (use a different file each time): ').strip().strip('"'))
            try:
                if any(path.resolve() == previous[0] for previous in summaries):
                    print('Choose a different file.')
                    continue
                with path.open(encoding='utf-8', newline='') as handle:
                    text = handle.read()
                break
            except (OSError, UnicodeError) as error:
                print(f'Cannot read file: {error}')
        codes, frequencies = build_codes(text)
        print(f'\nCode table for {path}')
        print(f'{"Character":12} {"Frequency":>10} Code')
        for char in sorted(codes):
            print(f'{repr(char):12} {frequencies[char]:10} {codes[char]}')
        bits = encode(text, codes)
        restored = decode(bits, codes)
        assert restored == text
        print('Encoded bit string:', bits)
        print('Decoded text equals original:', restored == text)
        summaries.append((path.resolve(), len(text) * 8, len(bits)))
    print(f'\n{"File":30} {"Fixed bits":>12} {"Huffman bits":>14} {"Fixed/Huffman":>15} {"Saved (%)":>12}')
    for path, fixed, compressed in summaries:
        ratio = f'{fixed / compressed:.4f}' if compressed else 'N/A'
        savings = f'{100 * (1 - compressed / fixed):.2f}' if fixed else 'N/A'
        print(f'{path.name:30} {fixed:12} {compressed:14} {ratio:>15} {savings:>12}')
    print('Ratios compare encoded payload bits with 8 bits per character; tree/code-table storage is excluded.')
    print('For non-ASCII text, the 8-bit-per-character baseline is hypothetical, not the UTF-8 file size.')


if __name__ == '__main__':
    main()
