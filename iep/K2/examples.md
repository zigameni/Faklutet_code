# Apache SPark Examples

## WordCount

Write a MapReduce program using Spark that reads the content of a given file and counts how many times each word appears in that file.

## Integral

Write a MapReduce program using Spark that calculates the integral of a function within given bounds.

## Matrix Multiplication

Write a MapReduce program using Spark that performs matrix multiplication on matrices read from a single file.

### Matrix multiplication in one step

The values entering the mapping are `A[i,j]` and `B[i,j]`, that is: `('A', i, j, A[i,j])` and `('B', i, j, B[i,j])`.

**What is the output of the mapping?**

The output of the reduction is `C[i,j]`, that is `('C', i, j, C[i,j])` where `C[i,j] = sum(k, A[I,k] * B[k,j])`.

**What is the input to the reduction?**

The input to the reduction is `A[i,*]` and `B[*,j]`.

**What is the key, and what is the value that comes?**

The key is `(i, j)`, and the value is `('A', k, A[i,k])` or `('B', k, B[k,j])`.

**Reduction based on:**

- Input `A[i,j]` gives multiple outputs where the key is `(i, k)` and the value is `('A', k, A[i,j])`.
- Input `B[i,j]` gives multiple outputs where the key is `(k, j)` and the value is `('B', k, B[j,j])`.

Write a MapReduce program that performs matrix multiplication on matrices read from a single file.

### Step 1:

```python
map(key, value):
    # value is ("A", i, j, a_ij) or ("B", j, k, b_jk) 
    if value[0] == "A":
        i = value[1]
        j = value[2]
        a_ij = value[3]
        emit(j, ("A", i, a_ij))
    else:
        j = value[1]
        k = value[2]
        b_jk = value[3]
        emit(j, ("B", k, b_jk))

reduce(key, values):
    # key is j
    # values is a list of ("A", i, a_ij) and ("B", k, b_jk)
    list_A = [(i, a_ij) for (M, i, a_ij) in values if M == "A"] 
    list_B = [(k, b_jk) for (M, k, b_jk) in values if M == "B"]
    for (i, a_ij) in list_A:
        for (k, b_jk) in list_B:
            emit((i, k), a_ij * b_jk)
```

### Step 2:

```python
map(key, value):
    emit(key, value)

reduce(key, values):
    result = 0
    for value in values:
        result += value
    emit(key, result)
```

## Movies 1

Write a MapReduce program using Spark that finds all the movies that had the same number of directors as the movie with the maximum number of directors.

## Movies 2

Write a MapReduce program using Spark that finds how many movies of each genre were released within a given time interval.

## Movies 3

Write a MapReduce program using Spark that finds the highest-rated movie that was both directed and written by the same person, and that was voted on by at least a certain number of users.

## Movies 4

Write a MapReduce program using Spark that finds the minimum number, maximum number, and average number of movies directed by someone.