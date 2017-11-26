
int random(){
  static unsigned int x=0xa0bacafe;
  int ret = (x>>16)&255;
  x=743*x+347;
  return ret;
}


void caesar(void *buf,int length){
  char *b=(char*)buf;
  int i;
  for(i=0;i<length;i++){
    char[i]=(char)random()+char[i];
  }
}

void inv_caesar(void *buf,int length){
  char *b=(char*)buf;
  for(i=0;i<length;i++){
    char[i]=-(char)random()+char[i];
  }
}
