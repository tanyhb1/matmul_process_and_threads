#include <mm_test.h>

#include <stdio.h>
#include <assert.h>
#include <stdlib.h>
#include <stdbool.h>
#include <stddef.h>
#include <time.h>
#include <ctype.h>
#include <sys/time.h>
#include <sys/mman.h>
#include <unistd.h>

// helper function to get each word from a line that i found online
// works by going through the line, if we see a word, add the pointer ot the first char to our array, process the char, once we reach the end of the char (Signified by a white space),
// we end the string by putting '\0'
// terminates at end of line when we reach a '\0'.
int getwords(char *line, char *words[], int maxwords)
{
  char *p = line;
  int nwords = 0;

  while(true)
    {
      while(isspace(*p))
	p++;

      if(*p == '\0')
	return nwords;

      words[nwords++] = p;

      while(!isspace(*p) && *p != '\0')
	p++;

      if(*p == '\0')
	return nwords;

      *p++ = '\0';

      if(nwords >= maxwords)
	return nwords;
    }
}

int main (int argc, char** argv) {

  assert (argc == 2);
  assert (argv);
  FILE * fp;
  char * line = NULL;
  size_t len = 0;
  ssize_t read;
  fp = fopen(argv[1], "r");
  if (fp == NULL)
    exit(EXIT_FAILURE);

  read = getline(&line, &len, fp);
  char* fst_line = line;
  int n = atoi(fst_line);

  int* matrixA = (int*) malloc(n * n * sizeof(int));
  int* matrixB = (int*) malloc(n * n *sizeof(int));
  int* matrixC = (int*) malloc(n * n *sizeof(int));
  int* matrixD = (int*) malloc(n * n *sizeof(int));
  int ai = 0;
  int bi = 0;
  int ci=0;
  int ctr = 0;

  while ((read = getline(&line, &len, fp)) != -1) {

    char **words = (char **) malloc ( n * 8);
    if (ctr < n){

      int nwords = getwords(line,words,n);
      for (int i=0; i<nwords;i++){
	matrixA[i + ai*n] = atoi(words[i]);
      }
      ai += 1;
    } else if (ctr >= n && ctr < n*2) {

      int nwords = getwords(line,words,n);
      for (int i=0; i<nwords;i++){
	matrixB[i + bi*n] = atoi(words[i]);
      }
      bi += 1;

    } else {

      int nwords = getwords(line, words, n);
      for (int i=0; i<nwords;i++){
	matrixC[i + ci*n] = atoi(words[i]);
      }
      ci+=1;  
    }
    ctr += 1;
  }

  /* time this */

  mm(n, matrixA, matrixB, matrixD);


  /* for (int i=0; i<n*n; i++){ */
  /*   //    printf("matrixc: %d, matrixd: %d\n", matrixC[i], matrixD[i]); */
  /*   assert(matrixC[i] == matrixD[i]); */
  /* } */

  // printing the output in format specified
  printf("%d\n", n);  
  for (int i=0; i<n; i++){
    //    printf("matrixc: %d, matrixd: %d\n", matrixC[i], matrixD[i]);
    for (int j=0; j<n-1; j++){
      printf("%d ", matrixA[j + i*n]);
    }
    printf("%d", matrixA[n-1 + i*n]);
    printf("\n");
  }
  for (int i=0; i<n; i++){
    //    printf("matrixc: %d, matrixd: %d\n", matrixC[i], matrixD[i]);
    for (int j=0; j<n-1; j++){
      printf("%d ", matrixB[j + i*n]);
    }
    printf("%d", matrixB[n-1 + i*n]);
    printf("\n");
  }

  for (int i=0; i<n; i++){
    //    printf("matrixc: %d, matrixd: %d\n", matrixC[i], matrixD[i]);
    for (int j=0; j<n-1; j++){
      printf("%d ", matrixD[j + i*n]);
    }
    printf("%d", matrixD[n-1 + i*n]);
    printf("\n");
  }

  //closing the file
  fclose(fp);
  if (line)
    free(line);
  exit(EXIT_SUCCESS);

}
