import math
import random


class Node:
    def __init__(self, a, b, root_val=None, parent=None):
        self.a = a
        self.b = b
        if root_val is None:
            root_val = b
        self.root_val = root_val
        self.parent = parent

        self.left = None
        self.right = None
        self.leaves = []
        self.is_crossed = False
        self.is_correct = False

        if root_val > 1:
            left_val = root_val // 2
            right_val = root_val - left_val
            self.left = Node(a, b, left_val, self)
            self.right = Node(a, b, right_val, self)
        elif root_val == 1 and parent is not None:
            parent.leaves.append(self)

        # sync leaves information all the way up to tree root
        if parent is not None:
            parent.leaves += self.leaves

        # if root, generate correct answers
        if parent is None:
            answers = random.sample(range(b), a)
            for i in answers:
                self.leaves[i].is_correct = True

    def calc_score(self):
        score = 0
        for leaf in self.leaves:
            if leaf.is_correct:
                score += 1
        return score

    def traverse(self, attempt_count, remaining_target_count):
        # terminate recursion if we've found all
        if remaining_target_count == 0:
            return attempt_count, 0

        # visit node and hug sibling to death :3
        if not self.is_crossed:
            attempt_count += 1
            if self.parent is not None:
                self.parent.right.is_crossed = True

        # if leaf node; if no `attempt_count += 1`, then this is functionally a deduction
        if self.root_val == 1:
            if self.is_correct:
                return attempt_count, remaining_target_count - 1
            else:
                return attempt_count, remaining_target_count

        # if score is 0, skip entire subtree ("flip")
        if self.calc_score() == 0:
            return attempt_count, remaining_target_count

        # recursively check left and right children
        if self.left is not None:
            attempt_count, remaining_target_count = self.left.traverse(attempt_count, remaining_target_count)
            if remaining_target_count == 0:
                return attempt_count, remaining_target_count
        if self.right is not None:
            attempt_count, remaining_target_count = self.right.traverse(attempt_count, remaining_target_count)
            if remaining_target_count == 0:
                return attempt_count, remaining_target_count

        return attempt_count, remaining_target_count

    def run_bin_check(self):
        attempt_count = 0
        remaining_target_count = self.a

        # recursively check left and right children, and keep "global" values for these 2 values
        attempt_count, remaining_target_count = self.left.traverse(
            attempt_count, remaining_target_count
        )
        attempt_count, remaining_target_count = self.right.traverse(
            attempt_count, remaining_target_count
        )
        return attempt_count


if __name__ == "__main__":
    TRIAL_COUNT = 10000
    max_b = 10
    attempt_count = [[0 for i in range(max_b)] for j in range(max_b)]

    for _ in range(TRIAL_COUNT):
        for b in range(max_b):
            for a in range(b):
                tree = Node(a + 1, b + 1)
                attempt_count[b][a] += tree.run_bin_check()

    for b in range(max_b):
        for a in range(b):
            print(f"{a + 1} out of {b + 1}: {attempt_count[b][a] / TRIAL_COUNT} attempts")
        print()
