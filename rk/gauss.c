#include <stdio.h>
#include <math.h>

void set_a(double a[6][6]){
  int i,j;
  for(i=0;i<6;i++){
    for(j=0;j<6;j++){
      a[i][j]=0;
    }
  }
  a[1][0]=1./4;
  a[2][0]=3./32;
  a[2][1]=9./32;
  a[3][0]=1932./2197;
  a[3][1]=-7200./2197;
  a[3][2]=7296./2197;
  a[4][0]=439./216;
  a[4][1]=-8.;
  a[4][2]=3680./513;
  a[4][3]=-845./4104;
  a[5][0]=-8./27;
  a[5][1]=2.;
  a[5][2]=-3544./2565;
  a[5][3]=1859./4104;
  a[5][4]=-11./40;
}

void set_b5(double b[6]){
  b[0]=16./135;
  b[1]=0.;
  b[2]=6656./12825;
  b[3]=28561./56430;
  b[4]=-9./50;
  b[5]=2./55;
}

void set_b4(double b[6]){
  b[0]=25./135;
  b[1]=0.;
  b[2]=1408./2565;
  b[3]=-2197./4104;
  b[4]=-1./5;
  b[5]=0.;
}

void set_c(double c[6]){
  c[0]=0.;
  c[1]=1./4;
  c[2]=3./8;
  c[3]=12./13;
  c[4]=1.;
  c[5]=1./2;
}


double f(double x){
  return exp(-x*x);
}

void rk_step(double x,double y,double h,double a[6][6],double b[6],double c[6],double *ynext){
  double fy[6],ysum,fysum=0;
  int i,j;
  for(i=0;i<6;i++){
    ysum=0;
    /*
    for(j=0;j<i;j++){
      ysum+=a[i][j]*fy[j];
    }
    */
    fy[i]=f(x+h*c[i]);
    fysum+=b[i]*fy[i];
  }
  *ynext=y+h*fysum;
}


double rk_main(double alpha,double epsilon,double h_init){
  double x=0,y=1,y4,y5,h=h_init;
  double a[6][6],b5[6],b4[6],c[6];
  set_a(a);
  set_b4(b4);
  set_b5(b5);
  set_c(c);
  printf("#\t%s\t%s\t%s\t%s\n","x","y","h","dy/dx");
  while(x<10.0){
    rk_step(x,y,h,a,b4,c,&y4);
    rk_step(x,y,h,a,b5,c,&y5);
    if(y4-y5<epsilon){
      printf("\t%f\t%f\t%e\t%f\n",x,y,h,f(x));
      x+=h;
      y=y5;
      h=alpha*h*pow(epsilon/fabs(y4-y5),0.2);
    }else{
      h=h/2;
    }
  }
  return y;
}

int main(){
  double y = rk_main(0.5,0.00005,0.001);
  fprintf(stderr,"%f: %f\n",y,sqrt(3.14159265359));
  return 0;
}
