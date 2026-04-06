#include<bits/stdc++.h>
using namespace std;
int b=0;
int a (int n){
    b=n+b;
    
    if(n<=0){
        return 0;
    }
    return a(n-1);

}

int c(int n,int suma){
    if (n<1){
        cout<<suma<<endl;
        return 0;
    }
    return c(n-1,suma+n);
}
int main(){
    // a(10);
    // cout<<b<<endl;

    c(10,0);
    return 0;
}