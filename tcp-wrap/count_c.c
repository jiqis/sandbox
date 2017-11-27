#include<stdio.h>
#include<string.h>
#include<stdlib.h>

#define BUFSIZE 8192
int main(){
	int c;
	int i=0,n=0;
	while((c=getchar())!=EOF){
		if(c=='c'||c=='C')i++;
		n++;
	}
	printf("%d Cs / %d characters\n",i,n);
	return 0;
}