#include <bits/stdc++.h>
using namespace std;
int binarysearch(const vector<int>& arr,int target){
    int left=0;
    int right=arr.size()-1;
    while(left<=right){
        int mid=(left+right)/2;
        if (arr[mid]==target){
            return mid;
        }
        if (arr[mid]<target){
            left=mid+1;
        }
        else{
            right=mid-1;
        }
    }
    return -1;
}
int main(){
    vector<int>nums={1,2,4,5,7,8,23,55,67};
    int target=8;
    int result_index=binarysearch(nums,target);
    if (result_index==-1){
        cout<<"element is not present"<<endl;
    }
    else{
        cout<<"element is present at index"<<result_index<<endl;
    }
    return 0;
}