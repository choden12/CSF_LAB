# Lab 7: Greedy and Randomized Algorithms

## Introduction
- This lab explores greedy and randomized algorithms for optimization, compression, graph processing, selection, and primality testing. It compares greedy choices with optimal solutions and examines how randomization affects correctness and performance.

## Objectives
- Implement and compare activity-selection rules.
- Compare fractional and 0/1 knapsack algorithms.
- Build Huffman codes and verify encoding and decoding.
- Implement Dijkstra’s, Kruskal’s, and Prim’s algorithms.
- Compare randomized quickselect with sorting.
- Compare Miller–Rabin primality testing with trial division.

## Tools and Technologies Used
- Python 3: Algorithm implementation.
- Visual Studio Code: Code editing.
- PowerShell: Program execution.
- heapq: Priority queues.
- random: Random inputs, pivots, and primality-test bases.
- time.perf_counter(): Measuring execution time.
- pathlib: Reading input files.
- collections.Counter: Counting character frequencies.

## Prerequisites
- Sorting, recursion, and complexity analysis.
- Greedy strategies and dynamic programming.
- Binary heaps and priority queues.
- Graph representations and shortest paths.
- Minimum spanning trees and union-find.
- Modular exponentiation and basic probability.

## Implementation
### Q1: Activity Selection and Knapsack
- Implemented earliest-finish, earliest-start, and shortest-duration activity selection. Random testing finds examples where the alternative rules select fewer activities than earliest finish.
- Implemented fractional knapsack using value-to-weight ratios. Compared the same greedy rule for 0/1 knapsack with a DP solution over 10,000 random inputs and reported the lowest observed greedy-to-optimal ratio.

## Q2: Huffman Coding
- Built Huffman trees from character frequencies using a priority queue. Printed code tables, encoded text into bit strings, and decoded the results.
- Verified that decoded text matched the original and compared encoded payload sizes with an 8-bit-per-character baseline for three different files.

## Q3: Shortest Paths and Minimum Spanning Trees
- Implemented heap-based Dijkstra’s algorithm to read a directed graph from a file and print distances and paths from a source.
- Implemented Kruskal’s algorithm with union-find and Prim’s algorithm with a heap. Verified matching MST weights on random connected graphs and benchmarked both for 1,000 vertices with 3,000 and 250,000 edges.
- Demonstrated a graph where adding one negative edge causes Dijkstra’s algorithm to return incorrect distances.

## Q4: Randomized Algorithms
- Implemented randomized quickselect and compared it with sorting and indexing for input sizes from 10,000 to 1,000,000.
Compared ten-round Miller–Rabin testing with trial division on 20 random 12-digit integers. Repeated one-round Miller–Rabin testing on 561 a thousand times and counted false “prime” answers.

## Screenshots and Evidence
Include screenshots showing:
1. Activity-selection counterexamples and knapsack comparisons.
![image](/images/LAB7A.png)
2. Huffman code tables, decoding verification, and compression ratios.
![image](/images/LAB7B.png)
3. Shortest paths, MST timing tables, and the negative-edge example.
![image](/images/LAB7C.png)
4. Quickselect timings, primality-test comparisons.
![image](/images/LAB7D.png)

## Challenges
- Choosing a greedy rule that produces an optimal result.
- Finding counterexamples through random testing.
- Distinguishing fractional knapsack from 0/1 knapsack.
- Handling equal character frequencies in Huffman trees.
- Preserving text exactly during encoding and decoding.

## Conclusion
- The lab demonstrated that greedy algorithms depend on the structure of the problem. Earliest-finish activity selection and fractional knapsack support optimal greedy choices, while ratio-based 0/1 knapsack can produce suboptimal results.
Huffman coding provided reversible text encoding, and Kruskal’s and Prim’s algorithms produced matching MST weights. Randomized quickselect returned correct order statistics, while Miller–Rabin demonstrated the distinction between probable primality and a guaranteed result.