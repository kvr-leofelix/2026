// #include <iostream>

// int main(){
//     std::cout<<"hello world "<<"\n";
//     std::cout<<"why on the earth"<<std::endl;
//     std::cout<<"hell";

// }

// -----------------------
// HOW TO REMOVE THE STD WORK
//  #include <iostream>
//  using namespace std;
//  int main(){
//     cout<<"hello";
//  }


// ----------------
// #include <iostream>
// using namespace std;
// int main(){
//     int x;
//     cin>>x;
//     cout<<"value of the x is: " <<x;
//     return 0;
// }

// #include <iostream>
// using namespace std;
// int main(){
//     int x,y;
//     cin>>x>>y;
//     cout<<"value of the x:"<<x<<"and y:"<<y;
//     return 0;
// }

// -------------------
// HOW TO INCLUDE ALL LIBRARY IN CPP IN ONE GO
// #include<bytes/stdc++.h>
// int store value from -2,14,74,83,648 to 2,14,74,83,647--4byte
//long --4byte
//unsigned long ==4byte
//unsigned short --2byte
// long long --8 byte
//float--4byte
//double--8 byte
//long double --10byte
//string and double
//c++--follow "minimum size" to remain efficient acrosss multiple devices
//int and long size are not define
// Data Type,Standard Minimum,Typical 32-bit System,Typical 64-bit System
// int,2byte,(4 bytes),(4 bytes)
// long,4byte,(4 bytes),(4/8 bytes)*
// long long,8byte,(8 bytes),(8 bytes)
//Note: On 64-bit Windows, long is usually 4 bytes. On 64-bit Linux or macOS, long is usually 8 bytes. This is a classic "gotcha" for developers moving code between platforms.


// #include<bits/stdc++.h>
// using namespace std;
// int main(){
//     string x;
//     cin>>x;
//     cout<<"this is the value you enter"<<x;
//     return 0;


// }

// #include<bits/stdc++.h>
// using namespace std;
// int main(){
//     string x;
//     getline(cin,x);
//     cout<<x;
//     return 0;
// }
// char is use to store character-256 are there
// #include<bits/stdc++.h>
// using namespace std;
// int main(){
//     int x;
//     cin>>x;
//     if(x>=20){
//         cout<<"you are adult";
//     }else if(x<20){
//         cout<<"you are kiddo";
//     }
//     return 0;
// }

// #include<bits/stdc++.h>.h>
// using namespace std;
// int main (){
//     int a;
//     cin>>a;
//     switch(a){
//         case 1:
//             cout<<"monday";
//             break;
//         case 2:
//             cout <<"tue";
//             break;
//         case 3:
//             cout<<"wed";
//             break;
//         case 4:
//             cout<<'thrush';
//             break;
//         default:
//             cout<<"invalid" 
//     }
//     cout<<"check";
//     return 0;
// }

// #include<bits/stdc++.h>
// using namespace std;
// int main (){
//     int arr[5];
//     cin >>arr[0]>>arr[1]>>arr[2]>>arr[3]>>arr[4];
//     cout <<arr[3];
//     for(int i = 0 ; i<5 ; i++){
//         cout<<arr[i]<<" ";
//     }
    

//     return 0;
// }

// #include<iostream>
// using namespace std;
// int main(){
//     int a[5]={1,2,3,4,5};
//     // for (int i=0;i<6;i++){
//     //     cout<<a[i];
//     // }
//     cout<<a[6];//this will give garbage value
//     return 0;
// }

// #include<bits/stdc++.h>
// using namespace std;
// int main(){
//     string a = "bittu";
//     int b = a.size();
//     a[b-1]='z';//use' not ""
//     cout<<a[b-1];
//     return 0;
// }

// #include<iostream>
// using namespace std;
// int main(){
//     for (int i;i<=5;i=i+1){
//         cout<<"striver"<<endl;
//     }
//     int i =5
//     while(i<=5){
//         cout<<"nittu"<<i<<endl;
//         i=i+1
//     }
//     return 0;

// }


// #include<iostream>
// using namespace std;
// int main(){
//     int i =2;
//     do{//this will run this part for minimum one time atlest
//         cout<<"striver"<<i<<endl;
//         i=i+1;
//     }while(i<=1);
//     cout<<i<<endl;
//     return 0;

// }

// #include<iostream>
// using namespace std;
// int sum(int num1,int num2){
//     int sum3=num1+num1;
//     return sum3
// }
// void printkaro(){
//     cout<<
//     void "this is kvr"
// }
// void printKaroWithParameter(string x){
//     cout<<"hey "<<x<<endl;
// }
// int main(){
//     int num1,num2;
//     cin>>num1>>num2;
//     int res=sum(num1,num2);
//     cout<<res;
//     printkaro();
//     printKaroWithParameter("bitty");
//     string a;
//     cin>>a;
//     printKaroWithParameter(a);
//     return 0;


// }

// #include<iostream>
// using namespace std;
// int maxx(int n1,int n2){
//     if (n1>=n2) return n1;
//     else return n2;

// }
// int main(){
//     int n1,n2;
//     cin>>n1>>n2;
//     int miinmum =maxx(n1,n2);
//     cout<<miinum;
//     return 0;
// }

//pass by value -- void a(string x){}
//pass by reference-- void a(&string x){}
//arrays always pass by refreence
#include<iostream>
using namespace std;
void sosome(int arr[],int n){
    arr[0]+=100;
    cout<<"vaule inside function :"<<arr[0]<<endl;
}
int main(){
    int n=5;
    int arr[n];
    for(int i=0;i<n;i+i+1){
        cin>>arr[1];
    }
    sosome(arr,n);
    cout<<"value inside the main"<<arr[0]<<endl;

}