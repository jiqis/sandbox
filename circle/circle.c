#include <stdio.h>
#include <math.h>
#define Sqr(x) ((x)*(x))
#define Len(v) (sqrt(Sqr((v).x)+Sqr((v).y)))
#define Inner(a,b) (((a).x*(b).x)+((a).y*(b).y)))
#define DT 0.00001
#define RESTI 1.0

#define E1 (1-RESTI)/2
#define E2 (1+RESTI)/2

typedef double Real;

typedef struct vector{
  Real x;
  Real y;
} Vector;

typedef struct circle{
  Real r;
  Vector v;
  Vector x;
} Circle;

void move(Circle *c, Real time){
  c->x.x+=c->v.x*time;
  c->x.y+=c->v.y*time;
}

Real time_strike(Circle c1,Circle c2){
  Real t=0;
  Real dt=DT;
  Real r2=Sqr(c1.r+c2.r);
  Real d2=Sqr(c1.x.x-c2.x.x)+Sqr(c1.x.y-c2.x.y),d2tmp;
  while((d2>r2)){
    move(&c1,dt);
    move(&c2,dt);
    t+=dt;
    if((d2tmp=Sqr(c1.x.x-c2.x.x)+Sqr(c1.x.y-c2.x.y))>d2){
      t=1.0/0.0;
      break;
    }
    d2=d2tmp;
  }
  return t;
}

Vector elemental(Vector x){
  Vector ret;
  Real len = Len(x);
  ret.x=x.x/len;
  ret.y=x.y/len;
  return ret;
}

Vector normal_vector(Vector l){
  Vector ret;
  ret.x=l.y;
  ret.y=-l.x;
  Real len = Len(ret);
  ret.x/=len;
  ret.y/=len;
  return ret;
}

int main(){
  Circle c1 = {2.0,{-1.0,0.0},{0.0,0.0}};
  Circle c2 = {2.0,{0.0,0.0},{10.0,0.0}};
  printf("%f\n",time_strike(c1,c2));
  return 0;
}

