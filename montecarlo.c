#include <stdio.h>
#include <time.h>
#include <stdlib.h>
#include <math.h>

/*DO NOT FORGET -lm*/

double random_(double max,double min){
  return (max-min)*((double)rand())/(RAND_MAX)+min;
}

double f(double x){
  return x;
}

int main(){
  int n=1000;
  double sum=0.0,sum2=0.0,y;
  int i;
  srand(time(NULL));
  for(i=0;i<n;i++){
    y=f(random_(1,0));
    sum+=y;
    sum2+=y*y;
  }
  printf("mean: %f,variant: %f\n",sum/n,(sum2/n-(sum/n)*(sum/n)));
  return 0;
}
