# matmul

Matrix Multiplication Benchmarks

## Task 1

  Write a mm_test.c program that do in order:
    - takes as an argument one of the test file,
    - Read the file from which it loads 3 matrices A,B and C
    - run mm(A,B,D) and make sure C == D
    - the ouput is formated the same as in test file,
      except that it is not N,A,B,C but N,A,B,D.   


## Task 2

   Edit the Makefile in order to run the tests.
   When we type make test, we expect to compile and run a tester for every single implementation of mm (mm_seq, mm_proc, mm_gol, etc...).


## Task 3

   Edit the Makefile so that when we type `make mmf_seq` instead of `make mm_seq`, then a floating point version of the matrix multiplication is compiled using the `-DDOUBLE_MM` preprocessing parameter.
