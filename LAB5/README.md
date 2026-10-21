# Lab 5: Sorting Algorithms

## Introduction
- This lab explores quicksort variants, counting sort, radix sort, and inversion counting. It compares their correctness and performance on different input sizes and distributions.

## Objectives
- Implement four quicksort variants and compare their execution times and comparison counts.
- Implement stable counting sort and LSD radix sort.
- Compare counting sort and radix sort with merge sort.
- Count inversions using brute force and merge sort.
- Calculate the Kendall tau distance between two movie rankings.

## Tools and Technologies Used
- Python 3
- Visual Studio Code
- Matplotlib
- random
- time.perf_counter()

## Prerequisites
- Arrays, loops, functions, and recursion.
- Divide-and-conquer algorithms.
- Sorting and time complexity analysis.
- Stable sorting and digit-based sorting.
- Inversions and ranking comparisons.

## Implementation
### Q1: Quicksort Variants
- Implemented Lomuto, Hoare, randomized, and three-way quicksort. Comparisons and execution times are measured for random, sorted, reverse-sorted, and duplicate-heavy arrays of sizes 1,000–16,000.
- Each variant recurses on the smaller partition and loops over the larger partition to limit recursion depth.

### Q2: Counting Sort and Radix Sort
- Implemented stable counting sort and LSD radix sort using bases 10 and 256. Counting sort is compared with merge sort for different key ranges, while radix sort is compared with merge sort for input sizes from 10,000 to 1,000,000.
- Execution times are plotted, and stability is demonstrated using (key, original index) pairs.

### Q3: Counting Inversions
- Implemented brute-force and merge-sort-based inversion counting. Their results are compared on random arrays up to size 2,000.
- Both methods are benchmarked on increasing input sizes. Brute force stops when its execution reaches approximately 60 seconds. Movie rankings entered from the keyboard are compared using Kendall tau distance.

## Screenshots and Evidence
Include screenshots showing:
1. Q1 comparison counts and execution-time tables.
![image](/images/LAB5A.png)
2. Q2 stability demonstration and benchmark plots.
![image](/images/LAB5B.png)
3. Q3 matching inversion counts, execution times, and movie-ranking distance.
![image](/images/LAB5C.png)

## Challenges
- Deep recursion on unbalanced quicksort partitions	Recurse on the smaller partition and loop on the larger one
Poor quicksort performance with repeated values	Use three-way partitioning to group equal keys
Preserving the order of equal keys	Place counting-sort elements from right to left.

## Conclusion
- The lab demonstrates how input order, duplicate values, and key ranges affect sorting performance. Random pivots reduce quicksort’s dependence on input order, while three-way partitioning handles duplicates efficiently.