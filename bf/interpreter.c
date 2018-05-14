#include<stdio.h>
#include<stdlib.h>
#include<time.h>
#define BUFSIZE 65536
#define STACKSIZE 64
void print_status(unsigned int p, unsigned int i, unsigned int max, unsigned char *buf, unsigned char *program,unsigned int sp, int stack[]){
	char recent[32],direction[31];
	int j,c=0;
	for(j=(i>=15)?(i-15):0;j<=i+15;j++){
		if(j>=max) {recent[j]=0;break;}
		recent[c]=program[j];
		c++;
	}
	recent[31]=0;
	c=((i>=15)?15:i)+10;
	for(j=0;j<c-1;j++) direction[j]=' ';
	direction[c-1]='^';
	direction[c]=0;
	fprintf(stderr,"status: current_instruction=%d,pointer=0x%x,mem[p]=%d,sp=%d\n",i,p,buf[p],sp);
	fprintf(stderr,"stack: ");
	for(j=0;j<sp;j++){
		fprintf(stderr,"%d",stack[j]);
		if(j!=sp-1)fprintf(stderr,", ");
	}
	fprintf(stderr,"\nprogram: %s\n%s\n",recent,direction);
}
void print_mem(unsigned int p,unsigned char *buf){
	unsigned int f=(p/256)*256;
	unsigned int i;
	for(i=f;i<f+256;i+=8){
		fprintf(stderr,"0x%02x: %02x %02x %02x %02x %02x %02x %02x %02x",i,buf[i],buf[i+1],buf[i+2],buf[i+3],buf[i+4],buf[i+5],buf[i+6],buf[i+7]);
		i+=8;
		fprintf(stderr," %02x %02x %02x %02x %02x %02x %02x %02x\n",buf[i],buf[i+1],buf[i+2],buf[i+3],buf[i+4],buf[i+5],buf[i+6],buf[i+7]);
	}
	fprintf(stderr,"pointer=0x%x\n",p);
}
int main(int argc, char** argv){
  srand((unsigned)time(NULL));
  unsigned char buf[BUFSIZE],program[BUFSIZE];
  int i=0,p=0,max=0,sp=0,bra=0;
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
    case '[': if(buf[p]>0){stack[sp]=i;sp++;i++;}else{bra=0;i++;while((program[i]!=']'||bra>0)&&i<max){if(program[i]=='[')bra++;if(program[i]==']')bra--;i++;}i++;}break;
    case ']': if(buf[p]>0){i=stack[sp-1]+1;}else{i++;sp--;}break;
	case '*': buf[p]=(int)((rand()/(1.0+RAND_MAX)*(buf[p]?buf[p]:256)));i++;break;
    case 's': print_status(p,i,max,buf,program,sp,stack);i++;break;
	case 'p': printf("%d",buf[p]);i++;break;
	case 'm': print_mem(p,buf);i++;break;
    default: i++;
    }
  }
  return 0;
}
	
