#include <stdio.h>
#include <time.h>
#include <stdlib.h>
#include <math.h>

#define PI 3.14159265359
#define sqr(x) ((x)*(x))
/*DO NOT FORGET -lm*/

double random_(double max,double min){
  return (max-min)*((double)rand())/(RAND_MAX)+min;
}

double f(){
  double sumcos,sumsin,theta,max,y;
  int i;
  theta=2.0*PI*random_(1,0);
  sumsin=sin(theta);
  sumcos=cos(theta);
  max=1.0;
  for(i=1;i<10;i++){
    theta=2.0*PI*random_(1,0);
    sumsin+=sin(theta);
    sumcos+=cos(theta);
    y=sqrt(sqr(sumcos)+sqr(sumsin));
    if(max<y) max=y;
  }
  return max;
}

int main(){
  int n=1000000;
  printf("n=%d\n",n);
  double sum=0.0,sum2=0.0,y;
  int i;
  srand(time(NULL));
  for(i=0;i<n;i++){
    y=(f()>=5.0)?1.0:0.0;
    sum+=y;
    sum2+=y*y;
  }
  double mean=sum/n;
  double variant=sum2/n-sqr(mean);
  double err=sqrt(variant/n);
  printf("mean: %f, variant: %f, standard error: %f\n",mean,variant,err);
  return 0;
}
