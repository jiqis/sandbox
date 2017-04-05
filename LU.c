#define N 5

void LU_decomposition(int n,double a[n][n]){
  int i,j,k;
  for(i=0;i<n;i++){
    /*TODO:枢軸選択*/
    a[i][i]=1./a[i][i];
    for(j=i+1;j<n;j++){
      a[j][i]=a[j][i]*a[i][i];
      for(k=i+1;k<n;k++){
	a[j][k]=a[j][k]-a[j][i]*a[i][k];
      }
    }
  }
}
