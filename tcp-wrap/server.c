#include<stdio.h>
#include<unistd.h>
#include<stdlib.h>
#include<string.h>
#include<sys/wait.h>
#include<sys/types.h>
#include<signal.h>
#include<sys/socket.h>
#include <arpa/inet.h>
#include <sys/select.h>
#include<sys/time.h>
#define BUFSIZE 8192
#define PORT 8080
#define output_log_wait(r,status,exit_code,process_name) if(r<0){perror("waitpid");}else if(WIFEXITED(status)){exit_code=WEXITSTATUS(status);fprintf(stderr,"child process '%s' exited successfully (%d)\n",process_name,exit_code);}else{fprintf(stderr,"%s: anormal child status: %04x\n",process_name,status);}

char filename[256] = "./test-program.exe";
int executer(int input,int output){
	int status;
	int exit_code;
	char buf[BUFSIZE];
	int pi[2],po[2];
	int count,i;
	if(pipe(pi)<0){
		perror("pipe");
		return -1;
	}
	if(pipe(po)<0){
		perror("pipe");
		return -1;
	}
	pid_t child_input=fork();
	if(child_input<0){
		perror("fork");
		return -1;
	}else if(child_input==0){
		close(pi[0]);
		close(po[1]);
		i=0;
		fprintf(stderr,"waiting input from client %d...\n",input);
		if((count=read(input,buf,BUFSIZE))>0){
			i=0;
			if(count<BUFSIZE) buf[count]=0;
			fprintf(stderr,"%s\n",buf);
			while(i<count) i+=write(pi[1],buf,count);
		}
		fprintf(stderr,"wrote %d byte\n",i);
		close(pi[1]);
		while((count=read(po[0],buf,BUFSIZE))>0){
			i=0;
			if(count<BUFSIZE) buf[count]=0;
			fprintf(stderr,">%s\n",buf);
			while(i<count) i+=write(output,&(buf[i]),count);
		}	
		close(po[0]);
		close(output);
		exit(0);
	}else{
		pid_t child_exec=fork();
		if(child_exec<0){
			perror("fork");
			kill(child_input,SIGINT);
			return -1;
		}else if(child_exec==0){
			close(pi[1]);
			close(po[0]);
			dup2(pi[0],0);
			dup2(po[1],1);
			close(input);
			if(input!=output) close(output);
			execl(filename,filename,NULL);
			perror("test");
			exit(-1);
		}else{
			close(pi[0]);
			close(pi[1]);
			close(po[0]);
			close(po[1]);
			pid_t r=waitpid(child_input,&status,0);
			output_log_wait(r,status,exit_code,"input");
			r=waitpid(child_exec,&status,0);
			output_log_wait(r,status,exit_code,"exec");			
		}
	}
	return 0;
}

int tcp_connection(){
	int lis = socket(PF_INET,SOCK_STREAM,0);
	if(lis<0){
		perror("socket");
		return -1;
	}
	struct sockaddr_in saddr,addr;
	int client;
	memset(&saddr,0,sizeof(struct sockaddr_in));
	saddr.sin_family=AF_INET;
	saddr.sin_addr.s_addr=htonl(INADDR_ANY);
	saddr.sin_port=htons(PORT);
	
	if(bind(lis,(struct sockaddr*)&saddr,sizeof(struct sockaddr))<0){
		perror("bind");
		return -1;
	}
	if(listen(lis,5)<0){
		perror("listen");
		return -1;
	}
	socklen_t addrlen=sizeof(addr);
	
	client = accept(lis,(struct sockaddr*)&addr,&addrlen);
	fprintf(stdout,"client: %d\n",client);
	if(client<0){
		perror("accept");
		return -1;
	}
	executer(client,client);
	close(lis);
	return 0;
	
}
int main(int argc,char** argv){
	if (argc>1){
		strcpy(filename,argv[1]);
		fprintf(stderr,"process: %s\n",filename);
	}
	tcp_connection();
	return 0;
}