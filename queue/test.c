#include <stdio.h>
#include "queue.h"

int main(){
  Queue_int q;
  int i,max;
  qi_init(&q);
  while(scanf("%d",&i)>0){
    qi_enqueue(&q,i);
  }
  max=qi_size(q);
  for(i=0;i<max;i++){
    printf("%d\n",qi_dequeue(&q));
  }
  return 0;
}
