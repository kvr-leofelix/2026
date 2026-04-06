// vector
//array have fixed number of entry we define at first but the vector is dynamic and its size alter with use
//emplace back is faster than push back

void exp_vector(){
    vector<int>v;
    v.push_back(1);
    v.emplace_back(2);
    vector<pair<int,int>>vec;
    vec.push_back({1,2});
    vec.emplace_back(1,2);//emplace_back dont need you give the entry in the format it auto change () to {()}
    vector<int>v(5,100);//[100,100,100,100,1001,100]
    vector<int>v(5);//[0,0,0,0,0]
    vector<int>v1(5,20);//define the v--> as [20,20,20,20,20]
    vector<int>v2(v1);//this copy the v1 to v2-->not the same v1 but the copy container of v1
    
    
    vector<int>::interator itt = v.begin();//v.begin() give the first address of the memory
    itt++;//this ++ move the memory address to next value which is 1*memory _size 
    cout <<*(itt)," ";
    itt=itt+2;//this * give the data store in that memeory address

    vector<int>::iterator it = v.end();//give the address just right after the last element in the vector .so to get the last element in the vector use it.end()-- to get the last element
    vector<int>::iterator it = v.rend();//reverse end so the end become first and the the element to give is the element just before the first element
    vector<int>::iterator it = v.rbegin();//reverse begin

    cout<<v[0]<<" "<<v.at(0);
    cout<<v.back()<<" ";
    

}