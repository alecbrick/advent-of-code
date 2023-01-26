from collections import deque


def part_1(order):
    circle = deque(order)
    num_moves = 100
    min_val = 1
    max_val = 9
    for i in range(num_moves):
        val = circle[0]
        circle.rotate(-1)
        removed = [circle.popleft(), circle.popleft(), circle.popleft()]
        new_label = val - 1
        while True:
            if new_label < min_val:
                new_label = max_val
                continue
            if new_label in removed:
                new_label -= 1
                continue
            break
        while circle[-1] != new_label:
            circle.rotate(-1)
        circle.extend(removed)
        while circle[-1] != val:
            circle.rotate(-1)
    while circle[0] != 1:
        circle.rotate()
    print(circle[1] * circle[2])


class Circle:
    def __init__(self, order):
        mapping = {}
        self.head = Node(order[0])
        self.prev = self.head
        mapping[self.head.val] = self.head
        for i in order[1:]:
            n = Node(i)
            self.prev.set_next(n)
            self.prev = n
            mapping[i] = n
        self.prev.set_next(self.head)
        self.mapping = mapping

    def __getitem__(self, item):
        return self.mapping[item]

    def remove_n_at(self, ind, n=1):
        to_remove = self.mapping[ind]
        ret = []
        for i in range(n):
            val = to_remove.remove()
            self.mapping.pop(val)
            to_remove = to_remove.next
            ret.append(val)
        return ret

    def extend_at(self, val, vals):
        to_extend = self.mapping[val]
        for v in vals:
            n = Node(v)
            self.mapping[v] = n
            to_extend.insert_after(n)
            to_extend = n


class Node:
    def __init__(self, val):
        self.val = val
        self.prev = None
        self.next = None

    def set_next(self, next):
        self.next = next
        next.prev = self

    def remove(self):
        self.prev.next = self.next
        self.next.prev = self.prev
        return self.val

    def insert_after(self, n):
        old_next = self.next
        self.next = n
        old_next.prev = n
        n.next = old_next
        n.prev = self


def part_2(order, num_moves=10000000, max_val=1000000):
    circle = Circle(order)
    min_val = 1
    curr = order[0]
    for i in range(num_moves):
        node = circle[curr]
        next_val = node.next.val
        removed = circle.remove_n_at(next_val, 3)
        new_label = curr - 1
        while True:
            if new_label < min_val:
                new_label = max_val
                continue
            if new_label in removed:
                new_label -= 1
                continue
            break
        circle.extend_at(new_label, removed)
        curr = node.next.val
    one_node = circle[1]
    after_1 = one_node.next.val
    after_2 = one_node.next.next.val
    print(f"{after_1} {after_2}")
    print(after_1 * after_2)


def main():
    order = [int(c) for c in "186524973"]
    order += [i for i in range(10, 1000001)]
    part_2(order)


if __name__ == "__main__":
    main()
