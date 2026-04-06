#include <iostream>
#include <vector>
#include <string>
#include <unordered_map>
#include <tuple>
#include <ctime>
#include <cstdlib>
#include <iomanip>



using namespace std;

struct PlayerRecord {
  string player_id;
  string name;
  int score;
  double timestamp;

  PlayerRecord(string a1, string a2, int sc, double ts)
      : player_id(a1), name(a2), score(sc), timestamp(ts) {}

  tuple<int, double, string> sortKey() {
    return make_tuple(-score, timestamp, player_id);
  }
};

struct SkipNode {
    tuple<int, double, string> key;
    PlayerRecord* player;
    vector<SkipNode*> fwd;

    SkipNode(int lvl, PlayerRecord* p = nullptr)
      : player(p), fwd(lvl + 1, nullptr) {
        if (p) key = p->sortKey();
    }
};

class SkipList_Board {
  int MAX_LVL = 16;
  double p_chance = 0.5;
  SkipNode* hdr;
  int cur_lvl;
  int sz;

public:
  unordered_map<string, PlayerRecord*> p_map;

    SkipList_Board() {
      hdr = new SkipNode(16);
      cur_lvl = 0;
      sz = 0;
    }

  int randLvl() {
      int n1 = 0;
      while ((double)rand() / RAND_MAX < p_chance && n1 < MAX_LVL)
        n1++;
      return n1;
  }

    vector<SkipNode*> buildUpd(tuple<int, double, string> k1) {
      vector<SkipNode*> upd(MAX_LVL + 1, nullptr);
      SkipNode* cur = hdr;
      for (int i = cur_lvl; i >= 0; i--) {
          while (cur->fwd[i] && cur->fwd[i]->key < k1)
            cur = cur->fwd[i];
          upd[i] = cur;
      }
      return upd;
    }

  void insertNode(PlayerRecord* p) {
      auto k1 = p->sortKey();
      auto upd = buildUpd(k1);
      int n_lvl = randLvl();
      if (n_lvl > cur_lvl) {
        for (int i = cur_lvl + 1; i <= n_lvl; i++)
            upd[i] = hdr;
        cur_lvl = n_lvl;
      }
      SkipNode* nd = new SkipNode(n_lvl, p);
      for (int i = 0; i <= n_lvl; i++) {
        nd->fwd[i] = upd[i]->fwd[i];
        upd[i]->fwd[i] = nd;
      }
      sz++;
  }

    bool removeNode(tuple<int, double, string> k1) {
      auto upd = buildUpd(k1);
      SkipNode* tgt = upd[0]->fwd[0];
      if (!tgt || tgt->key != k1) return false;
      for (int i = 0; i < (int)tgt->fwd.size(); i++) {
          if (upd[i]->fwd[i] != tgt) break;
          upd[i]->fwd[i] = tgt->fwd[i];
      }
      while (cur_lvl > 0 && !hdr->fwd[cur_lvl])
        cur_lvl--;
      sz--;
      return true;
    }

  void insertPlayer(string pid, string nm, int sc, double ts) {
      if (p_map.count(pid)) {
        cout << "[ERROR] Player '" << pid << "' already exists. Use updateScore().\n";
        return;
      }
      if (sc < 0 || sc > 10000) {
          cout << "[ERROR] Score must be in 0-10000.\n";
          return;
      }
      PlayerRecord* p = new PlayerRecord(pid, nm, sc, ts);
      p_map[pid] = p;
      insertNode(p);
      cout << "[INSERT] " << nm << " (ID:" << pid << ", Score:" << sc << ")\n";
  }

    void updateScore(string pid, int new_sc) {
        if (!p_map.count(pid)) {
          cout << "[ERROR] Player '" << pid << "' not found.\n";
          return;
        }
        if (new_sc < 0 || new_sc > 10000) {
            cout << "[ERROR] Score must be in 0-10000.\n";
            return;
        }
        PlayerRecord* p = p_map[pid];
        int old_s = p->score;
        removeNode(p->sortKey());
        p->score = new_sc;
        p->timestamp = (double)time(nullptr);
        insertNode(p);
        cout << "[UPDATE] " << p->name << ": " << old_s << " -> " << new_sc << "\n";
    }

  void deletePlayer(string pid) {
      if (!p_map.count(pid)) {
        cout << "[ERROR] Player '" << pid << "' not found.\n";
        return;
      }
      PlayerRecord* p = p_map[pid];
      p_map.erase(pid);
      removeNode(p->sortKey());
      cout << "[DELETE] " << p->name << " (ID:" << pid << ") removed.\n";
      delete p;
  }

    int getRank(string pid) {
      if (!p_map.count(pid)) return -1;
      auto t_key = p_map[pid]->sortKey();
      int rnk = 0;
      SkipNode* cur = hdr->fwd[0];
      while (cur) {
          rnk++;
          if (cur->key == t_key) return rnk;
          cur = cur->fwd[0];
      }
      return -1;
    }

  void searchPlayer(string pid) {
      if (!p_map.count(pid)) {
        cout << "[SEARCH] Player '" << pid << "' not found.\n";
        return;
      }
      PlayerRecord* p = p_map[pid];
      int r1 = getRank(pid);
      time_t ts = (time_t)p->timestamp;
      cout << "\n  [SEARCH RESULT]  ID:" << p->player_id
           << "  Name:" << p->name
           << "  Score:" << p->score
           << "  Rank:" << r1
           << "  Time:" << ctime(&ts);
  }

    vector<PlayerRecord*> getTopK(int k) {
      vector<PlayerRecord*> res;
      SkipNode* cur = hdr->fwd[0];
      int c1 = 0;
      while (cur && c1 < k) {
          res.push_back(cur->player);
          cur = cur->fwd[0];
          c1++;
      }
      cout << "\n" << string(52, '=') << "\n";
      cout << "  TOP " << k << " PLAYERS\n";
      cout << string(52, '=') << "\n";
      cout << "  " << left << setw(6) << "Rank"
           << setw(10) << "ID" << setw(16) << "Name" << setw(8) << "Score" << "\n";
      cout << "  " << string(44, '-') << "\n";
      for (int i = 0; i < (int)res.size(); i++) {
        PlayerRecord* p = res[i];
        cout << "  " << left << setw(6) << (i + 1)
             << setw(10) << p->player_id
             << setw(16) << p->name
             << setw(8) << p->score << "\n";
      }
      cout << string(52, '=') << "\n";
      return res;
    }

  void displayLeaderboard() {
      cout << "\n" << string(58, '=') << "\n";
      cout << "  LEADERBOARD  (" << sz << " players)\n";
      cout << string(58, '=') << "\n";
      cout << "  " << left << setw(6) << "Rank"
           << setw(10) << "ID" << setw(16) << "Name"
           << setw(8) << "Score" << "Time\n";
      cout << "  " << string(52, '-') << "\n";
      SkipNode* cur = hdr->fwd[0];
      int rnk = 1;
      while (cur) {
        PlayerRecord* p = cur->player;
        time_t ts = (time_t)p->timestamp;
        struct tm* t_info = localtime(&ts);
        char t_buf[10];
        strftime(t_buf, sizeof(t_buf), "%H:%M:%S", t_info);
        cout << "  " << left << setw(6) << rnk
             << setw(10) << p->player_id
             << setw(16) << p->name
             << setw(8) << p->score << t_buf << "\n";
        cur = cur->fwd[0];
        rnk++;
      }
      cout << string(58, '=') << "\n";
  }

    void displaySkipListStructure() {
        cout << "\n" << string(62, '=') << "\n";
        cout << "  SKIP LIST STRUCTURE  (levels 0.." << cur_lvl
             << ", " << sz << " nodes)\n";
        cout << string(62, '=') << "\n";
        if (sz == 0) {
          cout << "  (empty)\n";
          cout << string(62, '=') << "\n";
          return;
        }
        for (int lv = cur_lvl; lv >= 0; lv--) {
          cout << "  L" << lv << ": HEAD";
          SkipNode* n1 = hdr;
          while (n1->fwd[lv]) {
              n1 = n1->fwd[lv];
              cout << " -> [" << n1->player->name << ":" << n1->player->score << "]";
          }
          cout << " -> NIL\n";
        }
        cout << string(62, '=') << "\n";
    }
};

int main() {
  srand(42);
  SkipList_Board lb;
  double base = (double)time(nullptr);

  cout << string(62, '=') << "\n";
  cout << "  GAMING LEADERBOARD - Skip List Demo\n";
  cout << string(62, '=') << "\n";

    cout << "\n>>> OUTPUT 1: Insert, display, search, top-K\n\n";
    lb.insertPlayer("P01", "Mohit",   8500, base + 1);
    lb.insertPlayer("P02", "Sujal",     7200, base + 2);
    lb.insertPlayer("P03", "Shubham", 9100, base + 3);
    lb.insertPlayer("P04", "he",   8500, base + 4);
    lb.insertPlayer("P05", "she",     6800, base + 5);
    lb.insertPlayer("P06", "they",   9500, base + 6);
    lb.insertPlayer("P07", "vo",   7200, base + 7);

  lb.displayLeaderboard();
  lb.displaySkipListStructure();
  lb.searchPlayer("P03");
  lb.getTopK(3);

    cout << "\n>>> OUTPUT 2: Update, delete, edge cases\n\n";
    lb.updateScore("P02", 9800);
    lb.deletePlayer("P05");
    lb.displayLeaderboard();
    lb.displaySkipListStructure();

  cout << "\n";
  lb.searchPlayer("P02");
  int r2 = lb.getRank("P06");
  cout << "\n  they's rank after changes: " << r2 << "\n";

    lb.insertPlayer("P01", "mohit", 1000, base);
    lb.deletePlayer("P99");
    lb.searchPlayer("P99");

  return 0;
}
