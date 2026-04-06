// #include<bits/stdc++.h>
// using namespace std;

// void a(int m){
//     int c=0;
//     while(m>1){
//         m=m/10;
//         c=c;
        
        
//     }
//     cout<<c+1;

// }
// int main(){
//     int b;
//     cin>>b;
//     a(b);
//     return 0;
// }

#include<bits/stdc++.h>
using namespace std;

void a(int m){
    

}
int main(){
    for (int i=0;i<20;++i){
        int a = rand();
        int b =a;
        // cout<<"random number "<<i+1<<":"<<a<<endl;
        // Generate a random number between 1 and 100 (inclusive)
        // int random_number = (std::rand() % 100) + 1;
        int c=0;
        while(a>0){
          a=a/10;
          c=c+1;

        }
        cout<<"for "<<b<<" : "<<"number of digit "<<c<<endl;
    }
    return 0;
}