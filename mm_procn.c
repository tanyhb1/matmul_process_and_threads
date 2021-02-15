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

/* Set default NUM_PROCESSES to be 8 if not specified. User can specify via -DNUM_PROCESSES in gcc compilation */
#ifndef NUM_PROCESSES 
#define NUM_PROCESSES 8
#endif
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
  int i = 0; 
  int slice;
  int leftover = N % NUM_PROCESSES;
  if (leftover  == 0) { //account for when N cannot be perfectly divided by NUM_PROCESSES
    slice = N/NUM_PROCESSES;
    while (i < NUM_PROCESSES){
      int child_pid = fork();
      if (child_pid == 0){
	mm_helper(i*slice, (i+1)*slice, N, A,B,T);
	exit(0);
      }
      i++;
    }
    while(wait(NULL)>0);
    memcpy(C, T, sizeof(NUMTYPE) * N * N);
    munmap(T, N * N * sizeof (NUMTYPE));
  } else {
    slice = (N-leftover)/NUM_PROCESSES;
    while (i< NUM_PROCESSES ){
      int child_pid = fork();
      if (child_pid == 0){
	mm_helper(i*slice, (i+1)*slice, N, A,B,T);
	exit(0);
      }
      i++;
    }
    while(wait(NULL)>0);
    mm_helper(i*slice, (i*slice)+leftover,N,A,B,T);
    memcpy(C, T, sizeof(NUMTYPE) * N * N);
    munmap(T, N * N * sizeof (NUMTYPE));
  }



}
