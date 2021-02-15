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
struct arg_mm {
  size_t start;
  size_t end;
  size_t N;
  NUMTYPE * A;
  NUMTYPE * B;
  NUMTYPE * C;
};
pthread_mutex_t lock;
void * mm_helper (void* arguments) {
  pthread_mutex_lock(&lock);
  struct arg_mm *args = arguments;
  size_t N = args->N;
  NUMTYPE * A = args->A;
  NUMTYPE * B = args->B;
  NUMTYPE * C = args->C;
  printf("%ld %ld", args->start, args->end);
  for (unsigned int x = args->start ; x < args->end ; x++) {
    pthread_mutex_unlock(&lock);
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
      int atom = i++;
      args.start = atom*slice;
      args.end = (atom+1)*slice;
      rc = pthread_create(&(thread[atom]), NULL,  mm_helper , (void*) &args); // <--- segfaulting here
      assert(rc == 0);

    }    
    for(int i=0; i< NUM_THREADS; i++){
      printf("STOPPING THREADS: %d \n", i);
      rc= pthread_join(thread[i], NULL);
      assert(rc==0);
    }
    pthread_mutex_destroy(&lock);
  } else {
    slice = (N-leftover)/NUM_THREADS;
    struct arg_mm args;
    args.N = N;
    args.A = A;
    args.B = B;
    args.C = C;
    for (int i=0; i< NUM_THREADS; i++){
      args.start = i*slice;
      args.end = (i+1)*slice;
      rc = pthread_create(&thread[i], NULL, mm_helper, (void*) &args); // <--- segfaulting here
      
      assert(rc==0);
    }
    args.start = NUM_THREADS*slice;
    args.end = (NUM_THREADS*slice)+leftover;
    rc = pthread_create(&thread[NUM_THREADS], NULL, mm_helper,(void*) &args);

    for(int i=0; i <= NUM_THREADS; i++){
      rc = pthread_join(thread[i], NULL);
      assert(rc==0);
    }
    pthread_mutex_destroy(&lock);
  }
  

}
