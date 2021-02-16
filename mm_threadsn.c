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
#include <pthread.h>

/* Set default NUM_THREADS to be 8 if not specified. User can specify via -DNUM_THREADS in gcc compilation */
#ifndef NUM_THREADS
#define NUM_THREADS 8
#endif

pthread_mutex_t lock;
int curr_thread = 0;
struct arg_mm {
  size_t N;
  NUMTYPE * A;
  NUMTYPE * B;
  NUMTYPE * C;
};

void * mm_helper (void* arguments) {
  struct arg_mm *args = arguments;
  size_t N = args->N;
  NUMTYPE * A = args->A;
  NUMTYPE * B = args->B;
  NUMTYPE * C = args->C;

  //lock the critical section; might be instances where these values are changed before the current thread uses them, affecting correctness of the program
  pthread_mutex_lock(&lock);
  int i = curr_thread++;
  int start = i*N/NUM_THREADS;
  int end = (i+1) *N/NUM_THREADS;
  pthread_mutex_unlock(&lock);
  for (int x = start; x < end ; x++) {
    for (unsigned int y = 0 ; y < N ; y++) {
      unsigned int tidx = x + y * N ;
      C[tidx] = 0;
      for (unsigned int d = 0 ; d < N ; d++) {
	C[tidx] += A[d + y * N] * B[x + d * N] ;
      }
    }
  }

  return NULL;

}

void mm_seq (size_t start, size_t end, size_t N, NUMTYPE * A, NUMTYPE * B, NUMTYPE * C) {
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


void mm (size_t N, NUMTYPE * A, NUMTYPE * B , NUMTYPE * C) {

  int rc;
  pthread_t * thread = malloc(sizeof(pthread_t)*(NUM_THREADS+1));
  struct arg_mm args;
  args.N = N;
  args.A = A;
  args.B = B;
  args.C = C;
  int leftover = N%NUM_THREADS;
  for (int i =0; i< NUM_THREADS; i++){
    rc = pthread_create(&(thread[i]), NULL,  mm_helper , (void*) &args);
    assert(rc == 0);
  }
  for(int i=0; i< NUM_THREADS; i++){
    rc= pthread_join(thread[i], NULL);
    assert(rc==0);
  }
  pthread_mutex_destroy(&lock);
  if (leftover > 0){
    // handle the case where N/NUM_THREADS is not perfect, so we have to still account for the remainder.
    mm_seq(N-leftover, N, N, A,B,C);
  }
    
  

}
