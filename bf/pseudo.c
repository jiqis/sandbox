#include<stdio.h>
#include<stdlib.h>
#define BUFSIZE 65536
#define STACKSIZE 64
int main(int argc, char** argv){
  char buf[BUFSIZE];
  int program[BUFSIZE];
  int i=0,p=0,max=0,sp=0;
  int stack[STACKSIZE];
  FILE* f;
  if(argc>1){
    if((f=fopen(argv[1],"r"))==NULL){
      perror("open");
      return 0;
    }
  }else{
    f=stdin;
  }
  for(;i<BUFSIZE;i++){buf[i]=0;}
  i=0;
  while((p=getc(f))!=EOF){
    switch(p){
    case '+':
    case '-':
    case '>':
    case '<':
    case ',':
    case '.':
    case '[':
    case ']':
	case '*':
    case 's':
	case 'p':
	case 'm':program[i]=p;i++;
    }
    if(i%10==0&&i!=0) fprintf(stderr,"\nread %d bytes\n",i);
  }
  fprintf(stderr,"read %d bytes\n",i);
  fprintf(stderr,"program loading finished\n");
  max=i;
  i=0;
  p=0;
  while(i<max){
    switch(program[i]){
    case '+': buf[p]++; i++;break;
    case '-': buf[p]--; i++;break;
    case '>': p++; i++;break;
    case '<': p--; i++;break;
    case ',': buf[p]=(char)getchar(); i++;break;
    case '.': putchar((int)buf[p]);i++;break;
    case '[': if(buf[p]>0){stack[sp]=i;sp++;i++;}else{while(program[i]!=']'&&i<max)i++;i++;}break;
    case ']': if(buf[p]>0){sp--;i=stack[sp];}else{i++;}break;
    case 'd': fprintf(stderr,"*debug* recent=%d,pointer=%d,mem[p]=%d,program=%s\n",i,p,buf[p],program);i++;break;
    default: i++;
    }
  }
  return 0;
}
	
