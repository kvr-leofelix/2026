#include <iostream>
#include <string>
#include <unordered_map>
#include <unordered_set>
#include <vector>
#include <tuple>
#include <ctime>

using namespace std;

struct MsgNode {
    int msg_id;
    string sender_id;
    string text;
    double timestamp;
    bool is_deleted;
    unordered_set<string> del_for;
    MsgNode* prev;
    MsgNode* next;

    MsgNode(int id, string sid, string tx, double ts)
        : msg_id(id), sender_id(sid), text(tx), timestamp(ts),is_deleted(false), prev(nullptr), next(nullptr) {}
};

struct UndoEntry {
    string a1;
    int a2;
    string a3;
};

class MessagingSystem {
    double DEL_WIN = 120.0;
    MsgNode* head;
    MsgNode* tail;
    int sz;
    int next_id;

public:
    unordered_map<int, MsgNode*> msg_map;
    vector<UndoEntry> undo_stack;

    MessagingSystem()
      : head(nullptr), tail(nullptr), sz(0), next_id(1) {}

  int sendMessage(string sid, string tx, double ts) {
      int m_id = next_id++;
      MsgNode* nd = new MsgNode(m_id, sid, tx, ts);
      msg_map[m_id] = nd;

      if (!tail) {
        head = tail = nd;
      } else {
          nd->prev = tail;
          tail->next = nd;
          tail = nd;
      }
      sz++;

      time_t t1 = (time_t)nd->timestamp;
      struct tm* tm1 = localtime(&t1);
      char buf1[10];
      strftime(buf1, sizeof(buf1), "%H:%M:%S", tm1);
      cout << "[SENT] #" << m_id << " by " << sid
           << " at " << buf1 << ": \"" << tx << "\"\n";
      return m_id;
  }

    bool deleteForEveryone(int m_id, string req_id, double cur_time) {
        if (!msg_map.count(m_id)) {
          cout << "[ERROR] Message #" << m_id << " not found.\n";
          return false;
        }
        MsgNode* nd = msg_map[m_id];
        if (nd->sender_id != req_id) {
          cout << "[ERROR] Only the sender can delete for everyone.\n";
          return false;
        }
        if (nd->is_deleted) {
            cout << "[ERROR] Message #" << m_id << " already deleted for everyone.\n";
            return false;
        }
        double elapsed = cur_time - nd->timestamp;
        if (elapsed > DEL_WIN) {
          cout << "[ERROR] Time limit exceeded (" << (int)elapsed << "s > "
               << (int)DEL_WIN << "s). Cannot delete for everyone.\n";
          return false;
        }
        nd->is_deleted = true;
        undo_stack.push_back({"everyone", m_id, ""});
        cout << "[DEL-EVERYONE] Message #" << m_id << " deleted for everyone.\n";
        return true;
    }

  bool deleteForMe(int m_id, string u_id) {
      if (!msg_map.count(m_id)) {
        cout << "[ERROR] Message #" << m_id << " not found.\n";
        return false;
      }
      MsgNode* nd = msg_map[m_id];
      if (nd->del_for.count(u_id)) {
          cout << "[ERROR] Already hidden for " << u_id << ".\n";
          return false;
      }
      nd->del_for.insert(u_id);
      undo_stack.push_back({"forme", m_id, u_id});
      cout << "[DEL-FOR-ME] Message #" << m_id << " hidden for " << u_id << ".\n";
      return true;
  }

    void displayChat(string viewer_id = "") {
        string lbl = "  CHAT";
        if (!viewer_id.empty()) lbl += "  (viewer: " + viewer_id + ")";
        cout << "\n" << string(62, '=') << "\n";
        cout << lbl << "\n";
        cout << string(62, '=') << "\n";

      MsgNode* cur = head;
      int shown = 0;
      while (cur) {
          if (!viewer_id.empty() && cur->del_for.count(viewer_id)) {
            cur = cur->next;
            continue;
          }
          time_t t2 = (time_t)cur->timestamp;
          struct tm* tm2 = localtime(&t2);
          char buf2[10];
          strftime(buf2, sizeof(buf2), "%H:%M:%S", tm2);
          string body = cur->is_deleted ? "This message was deleted" : cur->text;
          cout << "  [" << buf2 << "] " << cur->sender_id
               << " (#" << cur->msg_id << "): \"" << body << "\"\n";
          shown++;
          cur = cur->next;
      }
      if (shown == 0)
          cout << "  (no messages)\n";
      cout << string(62, '=') << "\n";
    }

  bool undoLastDelete() {
      if (undo_stack.empty()) {
        cout << "[ERROR] Nothing to undo.\n";
        return false;
      }
      UndoEntry en1 = undo_stack.back();
      undo_stack.pop_back();

      if (en1.a1 == "everyone") {
          MsgNode* nd = msg_map[en1.a2];
          nd->is_deleted = false;
          cout << "[UNDO] Message #" << en1.a2 << " restored for everyone.\n";
      } else if (en1.a1 == "forme") {
        MsgNode* nd = msg_map[en1.a2];
        nd->del_for.erase(en1.a3);
        cout << "[UNDO] Message #" << en1.a2 << " restored for " << en1.a3 << ".\n";
      }
      return true;
  }
};

int main() {
    cout << string(62, '=') << "\n";
    cout << "  MESSAGING SYSTEM - Doubly Linked List Demo\n";
    cout << string(62, '=') << "\n";

  MessagingSystem chat;
  double base = (double)time(nullptr);

    cout << "\n>>> OUTPUT 1: Send, deleteForEveryone, displayChat\n\n";
    chat.sendMessage("Ali","Hey everyone!",base);
    chat.sendMessage("Baba","Hi Ali!",base + 5);
    chat.sendMessage("kri", "how ar u sup?",base + 10);
    chat.sendMessage("ali"," wrong message!", base + 15);
    chat.sendMessage("Baba","Meet at drongo 5 pm",base + 20);

  chat.displayChat();

  chat.deleteForEveryone(4, "Ali", base + 30);
  chat.displayChat();

    cout << "\n";
    chat.deleteForEveryone(1, "Ali", base + 200);

  cout << "\n>>> OUTPUT 2: deleteForMe, undo, multi-viewer\n\n";

    chat.deleteForMe(2, "kri");

  cout << "\n  -- kri's view --\n";
  chat.displayChat("kri");

    cout << "\n  -- Ali's view --\n";
    chat.displayChat("Ali");

  cout << "\n";
  chat.undoLastDelete();
  cout << "\n  -- kri's view after undo --\n";
  chat.displayChat("kri");

    cout << "\n";
    chat.undoLastDelete();
    chat.displayChat();

  return 0;
}
