#include<bits/stdc++.h>
using namespace std;
int test(int a){
    int count = 0;
    for(int i=1;i<=a;i++){
        if (a%i==0){
            count =count+1;
        }
    }
    if(count==2){
        cout<<"this is the prime number"<<endl;
    }else{
        cout<<"its NOT";
    }

}
int main(){
    int b;
    cin>>b;
    test(b);
    return 0;
}