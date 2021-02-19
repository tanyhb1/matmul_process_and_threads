/*
 * mm_seq.c
 *
 *  Created on: Jan 5, 2021
 *      Author: toky
 */


#include <stdio.h>
#include <assert.h>
#include <stdlib.h>
#include <stddef.h>
#include <mm_test.h>

void mm (size_t N, NUMTYPE * A, NUMTYPE * B, NUMTYPE * C) {
  unsigned int x,y,d;
#pragma omp parallel for shared(A,B,C) private(x,y,d)

  for ( x = 0 ; x < N ; x++) {
    for ( y = 0 ; y < N ; y++) {
      unsigned int tidx = x + y * N ;
      NUMTYPE tmp = 0;
      for ( d = 0 ; d < N ; d++) {
	  tmp += A[d + y * N] * B[x + d * N] ;
      }
      C[tidx] = tmp;
    }
  }
}


