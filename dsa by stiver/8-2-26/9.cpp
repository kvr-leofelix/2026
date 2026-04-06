#include<bits/stdc++.h>
using namespace std;

int test(int m,int n){
    vector<int> ls;
    for (int i=1;i<=min(m,n);i++){
        if((n%i==0)&&(m%i==0)){
            ls.push_back(i);
            // cout<<i<<"  ";

        }

    }
    
    for(auto it : ls)cout <<it<<" ";

}
int main(){
    int a,b;
    cin>>a>>b;
    test(a,b);
    return 0;
}
