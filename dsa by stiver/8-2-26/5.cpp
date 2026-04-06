#include<bits/stdc++.h>
using namespace std;
int test(int a){
    int f =a;
    int c=0;
    int e=0;
    while(a>0){
        int d=a%10;
        a=a/10;
        c=c+1;
        e=(e*10)+d;
    }
    // cout<<e<<endl;
    if (e==f){
        cout<<"its panindrome"<<endl;
    }else{
        cout<<"it is NOT"<<endl;
    }


}
int main(){
    int b;
    cin>>b;
    test(b);
    return 0;
}