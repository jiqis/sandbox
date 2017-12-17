#include <stdio.h>
#include <stdlib.h>
#include <time.h>
#include "matrix.h"
#define MIN(x,y) (((x)<(y))?(x):(y))

#define MAX(x,y) (((x)>(y))?(x):(y))

extern inline void mat_init(Matrix *mat,int m,int n){
  mat->body=(double*)malloc(m*n*sizeof(double));
  mat->raw=m;
  mat->column=n;
}
extern inline void mat_free(Matrix *mat){
  if(mat->body!=NULL)
    free(mat->body);
  mat->body=NULL;
  mat->raw=0;
  mat->column=0;
}

extern inline double mat_get(Matrix mat,int i,int j){
  if(i>=0&&i<mat.raw&&j>=0&&j<mat.column){
    return mat.body[i*mat.column+j];
  }else{
    return 0.;
  }
}
extern inline void mat_set(Matrix mat,int i,int j,double val){
  if(i>=0&&i<mat.raw&&j>=0&&j<mat.column){
    mat.body[i*mat.column+j]=val;
  }
}

extern inline Matrix mat_I(int m,int n){
  Matrix I;
  int i,j;
  mat_init(&I,m,n);
  for(i=0;i<m;i++){
    for(j=0;j<m;j++){
      if(i==j)
	mat_set(I,i,j,1.0);
      else
	mat_set(I,i,j,0.0);
    }
  }
  return I;
}

extern inline Matrix mat_rand(int m,int n){
  Matrix R;
  int i;
  srand(time(NULL)+rand());
  mat_init(&R,m,n);
  for(i=0;i<m*n;i++){
    R.body[i]=(double)(rand()%4);
  }
  return R;
}

extern inline Matrix mat_O(int m,int n){
  Matrix R;
  int i;
  srand(time(NULL)+rand());
  mat_init(&R,m,n);
  for(i=0;i<m*n;i++){
    R.body[i]=0.;
  }
  return R;
}

extern inline int mat_add(Matrix dest,Matrix a,Matrix b){
  int max=dest.raw*dest.column;
  int i;
  if(dest.raw==a.raw&&a.raw==b.raw&&dest.column==a.column&&a.column==b.column){
    for(i=0;i<max;i++){
      dest.body[i]=a.body[i]+b.body[i];
    }
    return 0;
  }else{
    fprintf(stderr,"Error:大きさの異なる行列で加法を行おうとしています\n");
    return -1;
  }
}

extern inline int mat_sub(Matrix dest,Matrix a,Matrix b){
  int max=dest.raw*dest.column;
  int i;
  if(dest.raw==a.raw&&a.raw==b.raw&&dest.column==a.column&&a.column==b.column){
    for(i=0;i<max;i++){
      dest.body[i]=a.body[i]-b.body[i];
    }
    return 0;
  }else{
    fprintf(stderr,"Error:大きさの異なる行列で減法を行おうとしています\n");
    return -1;
  }
}

extern inline int mat_mul(Matrix dest,Matrix a,Matrix b){
  int i,j,k;
  double s;
  if(dest.raw==a.raw&&dest.column==b.column&&a.column==b.raw){
    for(i=0;i<dest.raw;i++){
      for(j=0;j<dest.column;j++){
	s=0;
	for(k=0;k<a.column;k++){
	  s+=mat_get(a,i,k)*mat_get(b,k,j);
	}
	mat_set(dest,i,j,s);
      }
    }
    return 0;
  }else{
    fprintf(stderr,"Error:乗法を行おうとしている行列の大きさが合っていません\n");
    return -1;
  }
}

extern inline void mat_exchange(Matrix dest,int i,int j){
  int k;
  double s;
  for(k=0;k<dest.column;k++){
    s=mat_get(dest,i,k);
    mat_set(dest,i,k,mat_get(dest,j,k));
    mat_set(dest,j,k,s);
  }
}

extern inline void mat_cp(Matrix dest,Matrix src){
  int i;
  for(i=0;i<dest.raw*dest.column;i++){
    dest.body[i]=src.body[i];
  }
}

extern inline void mat_cp_lt(Matrix dest,Matrix src){
  int i,j;
  int r_max=MIN(dest.raw,src.raw);
  int c_max=MIN(dest.column,src.column);
  for(i=0;i<r_max;i++){
    for(j=0;j<c_max;j++){
      mat_set(dest,i,j,mat_get(src,i,j));
    }
  }
}

extern inline void mat_cp_rb(Matrix dest,Matrix src){
  int i,j;
  int r_max=MIN(dest.raw,src.raw);
  int c_max=MIN(dest.column,src.column);
  for(i=0;i<r_max;i++){
    for(j=0;j<c_max;j++){
      mat_set(dest,dest.raw-i-1,dest.column-j-1,mat_get(src,src.raw-i-1,src.column-j-1));
    }
  }
}

extern inline void mat_cp_lb(Matrix dest,Matrix src){
  int i,j;
  int r_max=MIN(dest.raw,src.raw);
  int c_max=MIN(dest.column,src.column);
  for(i=0;i<r_max;i++){
    for(j=0;j<c_max;j++){
      mat_set(dest,dest.raw-i-1,j,mat_get(src,src.raw-i-1,j));
    }
  }
}

extern inline void mat_cp_rt(Matrix dest,Matrix src){
  int i,j;
  int r_max=MIN(dest.raw,src.raw);
  int c_max=MIN(dest.column,src.column);
  for(i=0;i<r_max;i++){
    for(j=0;j<c_max;j++){
      mat_set(dest,i,dest.column-j-1,mat_get(src,i,src.column-j-1));
    }
  }
}

extern inline void mat_print(Matrix mat){
  int i,j;
  for(i=0;i<mat.raw;i++){
    for(j=0;j<mat.column;j++){
      printf("%f ",mat.body[i*mat.column+j]);
    }
    printf("\n");
  }
}
