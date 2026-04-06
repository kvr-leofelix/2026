#include <iostream>
#include <vector>
#include <queue>
using namespace std;

class solution{
    public:
    vector<int> bfsOfGraph(int V,vector<int> adj[]){
        int vis[V] = {0};
        vis[0] = 1;
        queue<int> q;
        q.push(0);
        vector<int> bfs;
        while(!q.empty()){
            int node = q.front();
            q.pop();
            bfs.push_back(node);
            for (auto it : adj[node]){
                if(!vis[it]){
                    vis[it] = 1;
                    q.push(it);
                }
            }
        }
        return bfs;
    }
};

int main(){
    int V = 5, E = 4;
    vector<int> adj[V];
    adj[0].push_back(1);
    adj[1].push_back(0);
    adj[0].push_back(2);
adj[2].push_back(0);
adj[0].push_back(3);
adj[3].push_back(0);
adj[2].push_back(4);
adj[4].push_back(2);
solution obj;
vector<int> result = obj.bfsOfGraph(V, adj);
cout << "bfs transverse";
for (int i: result){
    cout << i << " ";

}
cout << endl;
return 0;
}