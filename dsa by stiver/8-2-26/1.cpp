//to retrive the digit we do N%10 we get last digit N%100 last two digit
// #include<bits/stdc++.h>
// using namespace std;
// int main(){
//     int a = 7789.9;
//     int b = a%10;
//     cout<<b;
//     return 0; 
// }
#include<bits/stdc++.h>
using namespace std;
void good(int n){
    while(n>0){
        cout<<n%10<<endl;
        n=n/10;
    }
}

int main (){
    int a;
    cin>>a;
    good(a);
    return 0;
}