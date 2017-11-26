#include "queue.h"

void qi_init(Queue_int *q){
  q->now=0;
  q->head=0;
  q->size=0;
}

int qi_capacity(Queue_int q){
  return QUEUE_INT_MAX-q.size;
}

int qi_size(Queue_int q){
  return q.size;
}

void qi_enqueue(Queue_int *q,int i){
  if(qi_capacity(*q)>0){
    q->buf[q->now]=i;
    q->now=(q->now+1)%QUEUE_INT_MAX;
    q->size+=1;
  }else{
    q->buf[q->now]=i;
    q->now=(q->now+1)%QUEUE_INT_MAX;
    q->head=q->now;
  }
}

int qi_dequeue(Queue_int *q){
  int ret;
  if(q->size>0){
    ret=q->buf[q->head];
    q->head=(q->head+1)%QUEUE_INT_MAX;
    q->size-=1;
  }else{
  }
  return ret;
}

void qi_fin(Queue_int *q){
}
