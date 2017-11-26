#ifndef QUEUE_H
#define QUEUE_H
#define QUEUE_INT_MAX 8
typedef struct{
  int now;
  int head;
  int size;
  int buf[QUEUE_INT_MAX];
}Queue_int;

void qi_init(Queue_int *q);

int qi_capacity(Queue_int q);

void qi_enqueue(Queue_int *q,int i);

int qi_dequeue(Queue_int *q);

int qi_size(Queue_int q);

void qi_fin(Queue_int *q);
#endif
