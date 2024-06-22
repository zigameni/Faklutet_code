# Exercise Task

## Task Details
- A set of D = 64 files is given. The sizes of the files in [B] are as follows:
  ```
  s = (173669, 275487, 1197613, 1549805, 502334, 217684, 1796841, 274708,
  631252, 148665, 150254, 4784408, 344759, 440109, 4198037, 329673, 28602,
  144173, 1461469, 187895, 369313, 959307, 1482335, 2772513, 1313997, 254845,
  486167, 2667146, 264004, 297223, 94694, 1757457, 576203, 8577828, 498382,
  8478177, 123575, 4062389, 3001419, 196884, 617991, 421056, 3017627, 131936,
  1152730, 2676649, 656678, 4519834, 201919, 56080, 2142553, 326263, 8172117,
  2304253, 4761871, 205387, 6148422, 414559, 2893305, 2158562, 465972, 304078,
  1841018, 1915571)
  ```
- The goal is to optimize the use of memory with a size of 64 MiB = 2^26 B, for storing these files.
- The adopted representation of the solution to this problem is `x = (x1, x2,...xD)`, where `xk ∈ {0,1}` for `k = 1,2,...D` (0: the file is not stored, 1: the file is stored in the given memory).

## Optimization Function
The optimization function is defined as:

![img.png](img.png)


- The objective is to find the minimum (SAT class problem).

## Implementation
- Implement a genetic algorithm.
- Use a population size of 2000.
- The maximum number of iterations (calculations of the optimization function) is 100,000 per run, i.e., 50 generations.
- Perform 20 independent runs and save the optimization process (values of the optimization function in each iteration).
- Calculate and plot the cumulative minimum for each run (20 curves on one graph).
- Calculate and plot the average best solution based on the previous results.
- Present both graphs in log-log scale.
- The ASCII file accompanying the solution should contain a 64-bit string corresponding to the best-found solution and the minimum value of the optimization function (a solution satisfying `f(x) ≤ 32` is considered good enough).

## Example ASCII File Content
- 64-bit string of the best solution.
- Minimum value of the optimization function.
