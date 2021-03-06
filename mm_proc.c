#include <stdio.h>
#include <assert.h>
#include <stdlib.h>
#include <stddef.h>
#include <mm_test.h>
#include <sys/time.h>
#include <sys/mman.h>
#include <sys/wait.h>
#include <string.h>
#include <unistd.h>

void mm_helper (size_t start, size_t end, size_t N, NUMTYPE * A, NUMTYPE * B, NUMTYPE * C) {
  for (unsigned int x = start ; x < end ; x++) {
    for (unsigned int y = 0 ; y < N ; y++) {
      unsigned int tidx = x + y * N ;
      C[tidx] = 0;
      for (unsigned int d = 0 ; d < N ; d++) {
	  C[tidx] += A[d + y * N] * B[x + d * N] ;
      }
    }
  }
}

void mm ( size_t N, NUMTYPE * A, NUMTYPE * B, NUMTYPE * C) {
  int* T = mmap(NULL, N * N * sizeof (NUMTYPE),
		PROT_READ | PROT_WRITE, MAP_SHARED | MAP_ANONYMOUS,
		-1, 0);
  int child_pid = fork();
  if (child_pid == 0) {
    mm_helper(0, N/2, N, A, B, T);
    exit(0);
  } else {
    mm_helper(N/2, N, N, A, B, T);
  }
  wait(NULL);
  memcpy(C, T, sizeof(NUMTYPE) * N * N);
  munmap(T, N * N * sizeof (NUMTYPE));
}
