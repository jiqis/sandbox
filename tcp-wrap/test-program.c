#include<stdio.h>
#include<string.h>

#define BUFSIZE 8192
int main(){
	char buffer[8192];
	int c=0;
	int i,n;
	while(scanf("%s",buffer)>0){
		n=strlen(buffer);
		c+=n;
	}
	printf("%d letters",c);
	return 0;
}