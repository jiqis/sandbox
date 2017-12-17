#include<time.h>
#include<stdio.h>
short seed = 0;

void set_rand1(){
  seed=0;
  while(seed){
  seed = (short)time(NULL);
  }
}
short rand1(){
  seed = (short)((seed<<6)+(seed<<4)+(seed<<2)+seed+257)>>8;
  return seed;
}

int main(){
  set_rand1();
  long long int i=0;
  short init = rand1(),now;
  int occur[16]={};
  for(i=0;i<=10000000000;i++){
    if(init==(now=rand1())){
      printf("周期: %lld\n",i+1);
      return 0;
    }else{
      occur[(now>>4)&15]++;
    }
  }
  printf("周期 > 10000000000\n"); 
  return 0;
}
  
