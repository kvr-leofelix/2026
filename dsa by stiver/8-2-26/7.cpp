#include<bits/stdc++.h>
using namespace std;
int test(int m){
    // for(int i=1;i<=m;i++){
    //     if (m%i==0){
    //         cout<<i<<"  ";
    //     }
    // }
    vector<int> ls;
    for(int i=1;i<=sqrt(m);i++){
        if (m%i==0){
            cout<<i<<"  " <<m/i<<"  ";
            ls.push_back(i);
            if ((m/i)!=i){
                ls.push_back(m/i);
            }
        }
    }
    sort(ls.begin(),ls.end());
    for(auto it : ls) cout <<it << " ";

}
int main(){
    int a;
    cin >>a;
    test(a);
    return 0;
}