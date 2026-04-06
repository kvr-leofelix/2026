// NOTE WHEN GRAPH IS UNDIRECTIONAL 
#include <iostream>
#include <vector>
using namespace std;
int main(){
    int m, n;
    cin >> m >> n;
    vector<int> adj[n + 1];
    for (int i = 0; i < m;i++){
        int u, v;
        cin >> u, v;
        adj[u].push_back(v);
        adj[v].push_back(u);
    }
    return 0;
}

// --------------------------
// WHEN GRAPH IS DIRECTIONAL
#include <iostream>
#include <vector>
using namespace std;
int main(){
    int m, n;
    cin >> m >> n;
    vector<int> adj[n + 1];
    for (int i = 0; i < m;i++){
        int u, v;
        // U-->V
        cin >> u, v;
        adj[u].push_back(v);
        // adj[v].push_back(u);
    }
    return 0;
}
