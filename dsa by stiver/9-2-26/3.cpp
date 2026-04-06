#include<bits/stdc++.h>
using namespace std;

//string is multiletter , char is single letter
void a(int n,string m){//NOTE USE a(n-1,m) for recursion,"" use by string,'' use by char
    if(n<=0){
        return;
    }
    cout<<m<<endl;
    return a(n-1,m);

}

int aa =1;
void b(int n){
    cout<<aa<<endl;
    aa=aa+1;
    if(n<=1){
        return;
    }
    return b(n-1);
}

void c(int n){//to solve the earlier error which was int c(int n){}
    cout<<n<<endl;//either change the int c(int n)--> void c(int n) so that the return null can be justify
    if (n<=0){//or change the return --> return 0; while using int c(int n)
        return;
    }

    return c(n-1);
}






int main(){
    // #ifndef ONLINE_JUDGE
    // freopen("input.txt","r",stdin);
    // freopen("output.txt","w",stdout);
    // #endif
    // a(5,"leo");
    // b(10);
    c(10);
    return 0;

}