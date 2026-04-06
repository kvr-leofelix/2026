#include<bits/stdc++.h>
using namespace std;
int test(int a){
    int b = a;
    int c=0;
    int e=0;
    int f=0;
    while(a>0){
        int d=a%10;
        a=a/10;
        c=c+1;
        
        e = (e*10)+d;
        // f=f+(d*d*d);
        f=f+(pow(d,3));//through this way do the power NOTE ** is not define in c++
        cout<<f<<endl;

    }
    if(f==b){
        cout<<"they are armstrong"<<endl;
    }else{
        cout<<"they are NOT"<<endl;
    }

}
int main(){
    int b;
    cin>>b;
    test(b);
    return 0;
}