#include <vector>


class Node {
    public:
        Node(int a, int b, int rootVal, Node* parent);
        ~Node();

        int runBinCheck();

    private:
        int a;
        int b;
        int rootVal;
        bool isCrossed;
        bool isCorrect;

        Node* left;
        Node* right;
        Node* parent;
        std::vector<Node*> leaves;

        int calcScore();
        void traverse(int& attemptCount, int& remainingTargetCount);
};
