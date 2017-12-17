#ifndef MATRIX_H
#define MATRIX_H

typedef struct _matrix{
  double *body;
  int raw;
  int column;
} Matrix;

void mat_init(Matrix *mat,int m,int n);
void mat_free(Matrix *mat);

double mat_get(Matrix mat,int i,int j);
void mat_set(Matrix mat,int i,int j,double val);

Matrix mat_I(int m,int n);
Matrix mat_rand(int m,int n);
Matrix mat_O(int m,int n);


int mat_add(Matrix dest,Matrix a,Matrix b);
int mat_sub(Matrix dest,Matrix a,Matrix b);
int mat_mul(Matrix dest,Matrix a,Matrix b);
void mat_exchange(Matrix dest,int i,int j);
void mat_cp(Matrix dest,Matrix src);
void mat_cp_lt(Matrix dest,Matrix src);
void mat_cp_rb(Matrix dest,Matrix src);
void mat_cp_lb(Matrix dest,Matrix src);
void mat_cp_rt(Matrix dest,Matrix src);
void mat_print(Matrix mat);
#endif
