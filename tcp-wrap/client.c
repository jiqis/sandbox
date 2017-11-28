#include <unistd.h>
#include<stdio.h>
#include<sys/types.h>
#include<sys/socket.h>
#include <arpa/inet.h>
#include<string.h>
#include <sys/select.h>
#include<sys/time.h>

#define BUFSIZE 8192
#define PORT 8080
int  main(){
	int dest = socket(PF_INET,SOCK_STREAM,0);
	if(dest<0){
		perror("socket");
		return -1;
	}
	struct sockaddr_in saddr;
	memset(&saddr,0,sizeof(struct sockaddr_in));
	saddr.sin_family=AF_INET;
	saddr.sin_addr.s_addr=inet_addr("127.0.0.1");
	saddr.sin_port=htons(PORT);
	socklen_t addrlen=sizeof(saddr);
	if (connect(dest, (struct sockaddr *)&saddr,addrlen) > 0) {
		perror("connect");
		close(dest);
		return -1;
	}
	char buf[BUFSIZE];
	int w,n,i=0;
	fprintf(stderr,"connection success\n");
	fflush(stdout);
	if((n=read(0,buf,BUFSIZE))>0){
		if(n<BUFSIZE) buf[n]=0;
		while(i<n){
			if((w=write(dest,buf,n-i))<0) perror("write");
			else i+=w;
		}
	}
	fprintf(stderr,"wrote %d byte\n",n);
	int r;
	i=0;
	while((r=read(dest,&buf[i],BUFSIZE))>0){
		i+=r;
	}
	buf[i]=0;
	fprintf(stderr,"\e[34m%s\e[39m\n",buf);
	close(dest);
	return 0;
}
