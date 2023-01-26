import copy
from collections import defaultdict
from dataclasses import dataclass, field
from queue import PriorityQueue
from typing import Any

from utils.input import read_file, read_batches


DIRS = [">", "v", "<", "^"]


def parse_lines(lines):
    lines = lines[1:-1]
    lines = [line[1:-1] for line in lines]
    blizzards = defaultdict(list)
    for i, line in enumerate(lines):
        for j, c in enumerate(line):
            try:
                d = DIRS.index(c)
                blizzards[(i, j)].append(d)
            except ValueError:
                pass
    height = len(lines)
    width = len(lines[0])
    return blizzards, height, width

def move_blizzards(blizzards, height, width):
    new_blizzards = defaultdict(list)
    for pos, dirs in blizzards.items():
        for d in dirs:
            if d == 0:
                new_pos = (pos[0], (pos[1] + 1) % width)
            elif d == 1:
                new_pos = (pos[0] + 1) % height, pos[1]
            elif d == 2:
                new_pos = pos[0], (pos[1] - 1) % width
            else:
                new_pos = (pos[0] - 1) % height, pos[1]
            new_blizzards[new_pos].append(d)
    return new_blizzards


@dataclass(order=True)
class Step:
    priority: int
    item: Any = field(compare=False)


def navigate(start, end, blizzards, height, width):
    minute_to_blizzards = {0: blizzards}
    minute = 0
    queue = PriorityQueue()
    queue.put(Step(priority=minute, item=(start[0], start[1], minute)))
    visited = set()
    while queue.qsize() > 0:
        step = queue.get()
        y, x, minute = step.item
        print(queue.qsize(), y, x, minute)
        if y == end[0] and x == end[1]:
            print(f"Found! {minute + 1}")
            # one more blizzard progression
            blizzards = minute_to_blizzards[minute]
            new_blizzard = move_blizzards(blizzards, height, width)
            return minute + 1, new_blizzard
        if (y, x, minute) in visited:
            continue
        visited.add((y, x, minute))
        blizzards = minute_to_blizzards[minute]
        minute += 1
        if minute not in minute_to_blizzards:
            blizzards = move_blizzards(blizzards, height, width)
            minute_to_blizzards[minute] = blizzards
        else:
            blizzards = minute_to_blizzards[minute]
        if y == -1:
            possible_next = [(0, 0), (-1, 0)]
        elif y == height:
            possible_next = [(height - 1, width - 1), (height, width - 1)]
        else:
            possible_next = [(y, x + 1), (y + 1, x), (y, x - 1), (y - 1, x), (y, x)]
        for pos in possible_next:
            if pos in blizzards:
                continue
            if pos[0] < 0:
                if pos != (-1, 0):
                    continue
            if pos[0] >= height:
                if pos != (height, width - 1):
                    continue
            if pos[1] < 0 or pos[1] >= width:
                continue
            queue.put(Step(priority=minute, item=(pos[0], pos[1], minute)))
    print("Breaking. Hope it worked!")


def part_1():
    lines = read_file("input.txt")
    blizzards, height, width = parse_lines(lines)
    time_1, blizzards = navigate((-1, 0), (height - 1, width - 1), blizzards, height, width)
    time_2, blizzards = navigate((height, width - 1), (0, 0), blizzards, height, width)
    time_3, blizzards = navigate((-1, 0), (height - 1, width - 1), blizzards, height, width)
    print(time_1 + time_2 + time_3)



def part_2():
    lines = read_file("input.txt")


if __name__ == "__main__":
    part_1()
