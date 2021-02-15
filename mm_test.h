/*
 * mm_test.h
 *
 *  Created on: Jan 5, 2021
 *      Author: toky
 */

#ifndef _MM_TEST_H_
#define _MM_TEST_H_

#include <stddef.h>

#ifdef INTEGER_MM
#define NUMTYPE   int
#define NUMFORMAT "%d"
#define EPSILON   0
#endif

#ifdef DOUBLE_MM
#define NUMTYPE   long double
#define NUMFORMAT "%Lf"
#define EPSILON   0.0001
#endif

#ifndef NUMTYPE
#define NUMTYPE   int
#define NUMFORMAT "%d"
#define EPSILON   0
#endif

void mm (size_t N, NUMTYPE *A, NUMTYPE *B, NUMTYPE *C);



#endif /* MM_TEST_H_ */
