# Lab 6: Dynamic Programming

## Introduction
- This lab explores dynamic programming through rod cutting, matrix chain multiplication, longest common subsequence, and optimal binary search trees. It demonstrates how storing solutions to overlapping subproblems reduces repeated computation.

## Objectives
- Compare naive, memoized, and bottom-up rod-cutting algorithms.
- Find the optimal order of matrix multiplication.
- Compute and reconstruct a longest common subsequence.
- Use LCS to produce a line-by-line text diff.
- Construct an optimal binary search tree.

## Tools and Technologies Used
- Python 3: Algorithm implementation.
- Visual Studio Code: Code editing.
- PowerShell: Program execution.
- time.perf_counter(): Measuring execution time.
- random: Generating test inputs.
- pathlib: Reading text files.

## Prerequisites
- Recursion and basic complexity analysis.
- Lists and two-dimensional tables.
- Memoization and tabulation.
- Matrix multiplication.
- Strings, subsequences, and binary search trees.

## Implementation
### Q1: Rod Cutting
- Implemented naive recursion, top-down memoization, and bottom-up tabulation. Printed maximum revenues and piece lengths for rod lengths 1–10.
- Compared execution times and recursive-call counts for lengths 5, 10, 15, 20, and 25.

### Q2: Matrix Chain Multiplication
- Used bottom-up DP to calculate the minimum multiplication cost and reconstruct the optimal parenthesisation.
- Compared optimal costs with left-to-right multiplication and verified results using brute-force recursion for chains of up to eight matrices.

### Q3: Longest Common Subsequence
- Built and printed the LCS table for ABCBDAB and BDCABA, then reconstructed one LCS.
- Implemented a two-row version, compared DP with brute force for lengths 5–18, and used LCS to display differences between two text files.

### Q4: Optimal Binary Search Tree
- Computed the expected search cost using the given successful and unsuccessful search probabilities. Printed the optimal tree structure, including dummy leaves.


## Screenshots and Evidence
Include screenshots showing:
1. Rod-cutting revenues, piece lengths, recursive-call counts, and timings.
![image](/images/LAB6B.png)
2. Matrix-chain costs and optimal parenthesisations.
![image](/images/LAB6B.png)
3. The LCS table, reconstructed sequence, timing comparisons, and text diff.
![image](/images/LAB6C.png)
4. The optimal BST structure and expected search cost.
![image](/images/LAB6D.png)

## Challenges
- Identifying suitable subproblems and recurrence relations.
- Handling base cases and table boundaries correctly.
- Tracking recursive calls consistently across rod-cutting versions.

## Conclusion
- The lab demonstrated how dynamic programming avoids repeated computation by storing subproblem results. Memoization and tabulation improved rod-cutting efficiency, while matrix-chain DP found the least expensive multiplication order.