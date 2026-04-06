#include <iostream>

using namespace std;

// Task 1: Declare an array of size 10 and a top variable 
const int MAX_SIZE = 10;
int stack[MAX_SIZE];
int top = -1; // -1 indicates the stack is empty

// Task 11: Check if the stack is full [cite: 11]
bool isFull() {
    return top == MAX_SIZE - 1;
}

// Task 10: Check if the stack is empty [cite: 10]
bool isEmpty() {
    return top == -1;
}

// Task 2 & 14: Implement the push operation [cite: 7, 14]
void push(int value) {
    if (isFull()) {
        // Task 15: Display message if stack is full [cite: 15, 24]
        cout << "Stack Overflow! Cannot push " << value << ". The stack is full." << endl;
    } else {
        top++;
        stack[top] = value;
        cout << "Successfully pushed " << value << " onto the stack." << endl;
    }
}

// Task 3 & 16: Implement the pop operation [cite: 8, 16]
void pop() {
    if (isEmpty()) {
        // Task 17: Display message if stack is empty [cite: 17, 24]
        cout << "Stack Underflow! The stack is empty." << endl;
    } else {
        cout << "Popped element: " << stack[top] << endl;
        top--;
    }
}

// Task 4 & 18: Implement the display operation [cite: 9, 18]
void display() {
    if (isEmpty()) {
        cout << "The stack is currently empty." << endl;
    } else {
        cout << "Stack elements (Top to Bottom):" << endl;
        for (int i = top; i >= 0; i--) {
            cout << "| " << stack[i] << " |" << endl;
        }
        cout << " --- " << endl;
    }
}

// Task 5 & 19: Menu-driven approach [cite: 19, 21]
int main() {
    int choice, val;

    cout << "--- IC253 Stack Implementation Lab ---" << endl;

    do {
        cout << "\nChoose an operation:" << endl;
        cout << "1. Push" << endl;
        cout << "2. Pop" << endl;
        cout << "3. Display" << endl;
        cout << "4. Exit" << endl;
        cout << "Enter choice: ";
        cin >> choice;

        switch (choice) {
            case 1:
                cout << "Enter integer value to push: ";
                cin >> val; // [cite: 22]
                push(val);
                break;
            case 2:
                pop();
                break;
            case 3:
                display(); // [cite: 25]
                break;
            case 4:
                cout << "Exiting program..." << endl;
                break;
            default:
                cout << "Invalid choice! Please try again." << endl;
        }
    } while (choice != 4);

    return 0;
}