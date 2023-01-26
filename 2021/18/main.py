import json
import math

from utils.input import read_file


class Leaf:
    def __init__(self, n, height):
        self.n = n
        self.height = height

    def __str__(self):
        return f"{self.n}"

    def add_to_leftmost(self, n):
        self.n += n

    def add_to_rightmost(self, n):
        self.n += n

    def increment_height(self):
        self.height += 1

    def magnitude(self):
        return self.n


class Node:
    def __init__(self, left, right, height):
        if isinstance(left, int):
            self.left = Leaf(left, height + 1)
        else:
            self.left = Node(left[0], left[1], height + 1)
        if isinstance(right, int):
            self.right = Leaf(right, height + 1)
        else:
            self.right = Node(right[0], right[1], height + 1)
        if isinstance(left, int) and isinstance(right, int):
            self.is_pair = True
        else:
            self.is_pair = False
        self.height = height

    def __str__(self):
        return f"[{self.left}, {self.right}]"

    def add_to_leftmost(self, n):
        self.left.add_to_leftmost(n)

    def add_to_rightmost(self, n):
        self.right.add_to_rightmost(n)

    def explode(self):
        if self.height >= 4 and self.is_pair:
            return True, True, self.left.n, self.right.n
        if isinstance(self.left, Node):
            did_explode, just_exploded, left, right = self.left.explode()
            if just_exploded:
                self.left = Leaf(0, self.height + 1)
                if isinstance(self.right, Leaf):
                    self.is_pair = True
            if did_explode and right != 0:
                self.right.add_to_leftmost(right)
                return True, False, left, 0
            if did_explode:
                return True, False, left, right
        if isinstance(self.right, Node):
            did_explode, just_exploded, left, right = self.right.explode()
            if just_exploded:
                self.right = Leaf(0, self.height + 1)
                if isinstance(self.left, Leaf):
                    self.is_pair = True
            if did_explode and left != 0:
                self.left.add_to_rightmost(left)
                return True, False, 0, right
            if did_explode:
                return True, False, left, right
        return False, False, 0, 0

    def split(self):
        if isinstance(self.left, Leaf):
            if self.left.n >= 10:
                n = self.left.n
                self.left = Node(math.floor(n / 2), math.ceil(n / 2), self.height + 1)
                return True
        else:
            if self.left.split():
                return True
        if isinstance(self.right, Leaf):
            if self.right.n >= 10:
                n = self.right.n
                self.right = Node(math.floor(n / 2), math.ceil(n / 2), self.height + 1)
                return True
        else:
            if self.right.split():
                return True
        return False

    def magnitude(self):
        return self.left.magnitude() * 3 + self.right.magnitude() * 2

    def increment_height(self):
        self.height += 1
        self.left.increment_height()
        self.right.increment_height()


def parse_input(lines):
    ret = []
    for line in lines:
        lst = json.loads(line)
        ret.append(lst)
    return ret


def add_two_snailfish(left, right):
    new_node = Node(0, 0, 0)
    new_node.left = left
    new_node.left.increment_height()
    new_node.right = right
    new_node.right.increment_height()

    while True:
        did_explode, _, _, _ = new_node.explode()
        if did_explode:
            continue
        did_split = new_node.split()
        if did_split:
            continue
        break
    return new_node


def add_snailfish(lines):
    curr = lines[0]
    curr = Node(curr[0], curr[1], 0)
    for num in lines[1:]:
        num = Node(num[0], num[1], 0)
        curr = add_two_snailfish(curr, num)
    return curr


def part_1():
    lines = read_file("input.txt")
    lines = parse_input(lines)

    total = add_snailfish(lines)
    print(total.magnitude())


def part_2():
    lines = read_file("input.txt")
    lines = parse_input(lines)
    max_magnitude = 0
    for i in range(len(lines) - 1):
        for j in range(i + 1, len(lines)):
            a = lines[i]
            tree_a = Node(a[0], a[1], 0)
            b = lines[j]
            tree_b = Node(b[0], b[1], 0)
            total = add_two_snailfish(tree_a, tree_b)
            mag = total.magnitude()
            if mag > max_magnitude:
                max_magnitude = mag

            tree_a = Node(a[0], a[1], 0)
            tree_b = Node(b[0], b[1], 0)
            total = add_two_snailfish(tree_b, tree_a)
            mag = total.magnitude()
            if mag > max_magnitude:
                max_magnitude = mag
    print(max_magnitude)


if __name__ == "__main__":
    part_2()
