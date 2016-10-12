#include <stdio.h>


struct pos {
  int x;
  int y;
};

struct pos add(struct pos a,struct pos b){
  struct pos ret = {a.x+b.x,a.y+b.y};
  return ret;
}

int main(){
  struct pos a={1,2};
  struct pos b={a.x+4,a.y+3};

  printf("(%d,%d)\n",b.x,b.y);
  return 0;
}