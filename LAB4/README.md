# Lab 4: Modular and Matrix Exponentiation

## Introduction
- Exponentiation calculates a number or matrix raised to a given power. Repeated multiplication becomes slow for large exponents. Binary exponentiation improves efficiency by repeatedly squaring the base and processing the exponent’s binary digits. 

- This lab implements naive and binary exponentiation with modular arithmetic. Matrix exponentiation is then applied to Fibonacci numbers and counting walks in directed graphs.

## Objectives
- Implement naive, binary, and bitwise modular exponentiation.
- Handle zero exponents, negative bases, and invalid inputs.
- Implement matrix multiplication and identity matrices.
- Compare naive and binary matrix exponentiation.
- Calculate Fibonacci numbers using matrix exponentiation.
- Count directed walks using adjacency matrices.
- Measure and compare execution times.

## Tools and Technologies Used
- Tool	
- Python 3	
- Visual Studio Code	
- time.perf_counter()
- random module	

## Prerequisites
**The lab requires an understanding of:**
- Modular arithmetic.
- Loops, functions, and bitwise operations.
- Square matrices and matrix multiplication.
- Identity matrices.
- Fibonacci sequences.
- Directed graphs and adjacency matrices.
- Basic time complexity analysis.

## Implementation
### Part A: Modular Exponentiation
1. Implement naive, binary, and bitwise exponentiation.
2. Validate inputs and handle special cases.
3. Compare outputs and execution times for exponents from 10 to 10⁶.

### Part B: Matrix Exponentiation
1. Implement matrix multiplication, identity matrices, and both exponentiation methods.
2. Compare outputs for different matrices, exponents, and moduli.
3. Calculate Fibonacci numbers and count directed graph walks.
4. Benchmark dimensions 2–32 and exponents 2⁴–2¹².


## Screenshots and Evidence
The following terminal outputs provide execution evidence. Screenshots of these outputs can be included when preparing the final submission.
#### Modular Exponentiation Output
![image](/images/LAB4A.png)

#### Matrix Exponentiation Output
![image](/images/LAB4B.png)

## Challenges 
- Large exponents require many multiplications	Use repeated squaring
- Intermediate values grow rapidly	Reduce modulo m during computation
- Zero exponent requires special handling	Initialize with 1 % m or the reduced identity matrix

## Conclusion
- The lab demonstrated that naive and binary exponentiation produce the same results while requiring different amounts of computation. Binary exponentiation reduces the number of multiplications from linear to logarithmic growth in the exponent.