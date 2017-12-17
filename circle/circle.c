#include <stdio.h>
#include <math.h>
/*ここでReal型をFLOATにするかDOUBLEにするか指定する*/
#define DOUBLE

#define Sqr(x) ((x)*(x))
#define Len(v) (sqrt(Sqr((v).x)+Sqr((v).y)))
#define Inner(a,b) (((a).x*(b).x)+((a).y*(b).y)))
#define DT 0.00001
#define RESTI 1.0
#define E1 (1-RESTI)/2
#define E2 (1+RESTI)/2

#ifdef DOUBLE
typedef double Real;
#define Sqrt(x) sqrt(x)
#define INF Sqr(Sqr(Sqr(Sqr(Sqr(Sqr(Sqr(Sqr(65536.0))))))))
#endif

#ifdef FLOAT
typedef float Real;
#define Sqrt(x) sqrtf(x);
#define INF Sqr(Sqr(Sqr(Sqr(Sqr(65536.0)))))
#endif

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

int Discriminant(Real a,Real b,Real c){
  return Sqr(b)-4.0*a*c;
}

Vector quadratic(Real a,Real b,Real c){
  Vector root;
  Real discr = Sqr(b)-4.0*a*c;
  /*大きい方の解*/
  root.x=(-b+Sqrt(discr))/(2.0*a);
  /*小さい方の解*/
  root.y=(-b-Sqrt(discr))/(2.0*a);
  return root;
}

Real time_hit(Circle c1,Circle c2){
  Circle d;
  Vector root;
  d.x.x=c1.x.x-c2.x.x; d.x.y=c1.x.y-c2.x.y;
  d.v.x=c1.v.x-c2-v.x; d.v.y=c1.v.y-c2.v.y;
  d.r=c1.r+c2.r;
  Real a=Sqr(d.v.x)+Sqr(d.v.y),b=2.0*(d.v.x*d.x.x+d.v.y*d.x.y),c=Sqr(d.x.x)+Sqr(d.x.y)-d.r;
  if((d.v.x==0.0&&d.v.y==0.0)||(discriminant(a,b,c)){
    return INF;
  }else{
    root=quadratic(a,b,c);
    if(root.y>=0.0){
      return root.y;
    }else if(root.x>=0){
      return root.x;
    }else{
      return INF;
    }
  }
  return t;
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

