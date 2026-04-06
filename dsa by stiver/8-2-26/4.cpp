#include<bits/stdc++.h>
using namespace std;
int test(int m){
    int b =0;
    int c=0;
    while(m>0){
        int d;
        d=m%10;
        m=m/10;
        b=b+1;
        c=(c*10)+d;
        
    }
    return c;

}
int main(){
    int a ;
    cin>>a;
    int h=test(a);
    cout<<h<<endl;
    return 0;
}