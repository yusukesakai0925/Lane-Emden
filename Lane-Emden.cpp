#include<iostream>
#include<cmath>
#include<limits>

int main(){
  double n=3;
  double gzi_zero=0.00000001;  //初期gzi
  
  double y1=1-1/6*gzi_zero*gzi_zero+n/120*gzi_zero*gzi_zero*gzi_zero*gzi_zero;
  double y2=-1/3*gzi_zero+n/30*gzi_zero*gzi_zero*gzi_zero;
  double gzi=gzi_zero;

  double dgzi=0.00001;
  double gzimax=20.0;

  double k1,k2,k3,k4;
  
  for(int i=0;i<int(gzimax/dgzi);i++){
    y1+=y2*dgzi;
    k1=(-pow(y1,n)-2/gzi*y2)*dgzi;
    k2=(-pow(y1,n)-2/(gzi+dgzi/2)*(y2+k1/2))*dgzi;
    k3=(-pow(y1,n)-2/(gzi+dgzi/2)*(y2+k2/2))*dgzi;
    k4=(-pow(y1,n)-2/(gzi+dgzi)*(y2+k3))*dgzi;
    //std::cout<<k1<<" "<<k2<<" "<<k3<<" "<<k4<<std::endl;
    y2+=1.0/6.0*(k1+2*k2+2*k3+k4);
    gzi+=dgzi;
    if(isnan(y1)) break;
    std::cout<<gzi<<" "<<y1<<" "<<y2<<std::endl;
}
  return 0;
}
