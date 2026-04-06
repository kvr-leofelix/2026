#include<bits/stdc++.h>
using namespace std;
int count(int n){
    int cnt = (int)(log10(n)+1);
    return cnt;
}
//if division is by 2 use log2 ,if it is by 5 use log5,if it is division by 100 use log100
