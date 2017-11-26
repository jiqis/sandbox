#include "matrix.h"
#include <stdio.h>
#define N 2
#define M 4
#define L 3
int main(){
  Matrix m1,m2,result;
  m1=mat_rand(N,M);
  m2=mat_rand(M,L);
  mat_init(&result,N,L);
  mat_print(m1);
  putchar('\n');
  mat_print(m2);
  putchar('\n');
  mat_mul(result,m1,m2);
  mat_print(result);
  putchar('\n');
  mat_free(&m1);
  mat_free(&m2);
  mat_free(&result);
  return 0;
}
