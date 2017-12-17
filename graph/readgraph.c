#include<stdio.h>
#include<stdlib.h>
#define EMPTY -2147483647-1
typedef struct node{
	char[32] name;
	int id;
} Node;

typedef struct edge{
	int from;
	int to;
	int cost;
} Edge;

typedef struct list_node{
	Node n;
	struct list_node *next;
	int len;
} Nodes;

int init_list(Nodes *l){
	l=(Nodes*)malloc(sizeof(Nodes));
	if(l==NULL) return -1;
	l->next=NULL;
	l->n={}
	l->len=0;
	return 0;
}
int isempty(Nodes *l){
	if(l==NULL) return (0==0);
	return (l->next==NULL);
}
int fin_list(Nodes *l){
	if(l==NULL) return 0;
	else if(isempty(l)){
		free(l);
		return 0;
	}else{
		fin_list(l);
		free(l);
		return 0;
	}
	return -1;
}
void push_list(Nodes *l,Node n){
	Nodes *next;
	init_list(next);
	*next=*l;
	l->next=next;
	l->n=n;
	l->len=next->len+1;
}

int main(){
	return 0;
}