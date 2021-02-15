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
  int i = curr_thread++;
  if (N % NUM_THREADS != 0 && i == NUM_THREADS){
    int leftover = N%NUM_THREADS;
    for (unsigned int x = N-leftover ; x < N ; x++) {
      for (unsigned int y = 0 ; y < N ; y++) {
	unsigned int tidx = x + y * N ;
	C[tidx] = 0;
	for (unsigned int d = 0 ; d < N ; d++) {
	  C[tidx] += A[d + y * N] * B[x + d * N] ;
	}
      }
    }
  } else
    {
      for (unsigned int x = i * N / NUM_THREADS ; x < (i+1)*N/NUM_THREADS ; x++) {
	for (unsigned int y = 0 ; y < N ; y++) {
	  unsigned int tidx = x + y * N ;
	  C[tidx] = 0;
	  for (unsigned int d = 0 ; d < N ; d++) {
	    C[tidx] += A[d + y * N] * B[x + d * N] ;
	  }
	}
      }}

  return NULL;

}
void mm (size_t N, NUMTYPE * A, NUMTYPE * B , NUMTYPE * C) {

  int slice, rc;
  int leftover = N % NUM_THREADS;
  pthread_t * thread = malloc(sizeof(pthread_t)*(NUM_THREADS+1));
  if (leftover  == 0) { //account for when N cannot be perfectly divided by NUM_THREADS
    slice = N/NUM_THREADS;
    struct arg_mm args;
    args.N = N;
    args.A = A;
    args.B = B;
    args.C = C;
    int i = 0;
    while (i < NUM_THREADS){
      printf("NOW AT %d WITH START %d and END %d\n", i, i*slice, (i+1)*slice);
      rc = pthread_create(&(thread[i]), NULL,  mm_helper , (void*) &args); // <--- segfaulting here
      i++;      
      assert(rc == 0);

    }
    
    for(int i=0; i< NUM_THREADS; i++){
      printf("STOPPING THREADS: %d \n", i);
      rc= pthread_join(thread[i], NULL);
      assert(rc==0);
    }

  } else {
    slice = (N-leftover)/NUM_THREADS;
    struct arg_mm args;
    args.N = N;
    args.A = A;
    args.B = B;
    args.C = C;
    for (int i=0; i< NUM_THREADS; i++){
      rc = pthread_create(&thread[i], NULL, mm_helper, (void*) &args); // <--- segfaulting here
      
      assert(rc==0);
    }
    rc = pthread_create(&thread[NUM_THREADS], NULL, mm_helper,(void*) &args);

    for(int i=0; i <= NUM_THREADS; i++){
      rc = pthread_join(thread[i], NULL);
      assert(rc==0);

    }

  }
  

}
