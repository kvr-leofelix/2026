#include<bits/stdc++.h>
using namespace std;

void a(int n){
    if(n<0){
        return;
    }
    cout<<"hello "<<n<<endl;
    return a(n-1);
}
int main(){
    a(10);
}