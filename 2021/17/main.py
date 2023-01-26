import math
import heapq

from utils.input import read_file


def parse_input(line):
    _, right = line.split(": ")
    x, y = right.split(", ")
    x1, x2 = x.split("=")[1].split("..")
    y1, y2 = y.split("=")[1].split("..")
    return int(x1), int(x2), int(y1), int(y2)


def part_1():
    _input = read_file("input.txt")[0]
    x1, x2, y1, y2 = parse_input(_input)
    print(f"{x1} {x2} {y1} {y2}")

    # We know that after some time, after y velocity decreases to -y, our current y position will be 0.
    # After that, the distance to the target is going to be, e.g. if the initial velocity is 10:
    # 11 + 12 + 13 + 14 + ... + n.
    # So, what's our target? -76 to -48?
    # That means we _do_ pass through the target: when n = 14 and 15.
    # When _can't_ it pass through the target?
    # When y = -77.
    # So we should start at y = -76, and figure out if there's an X that allows for that.
    # When is there an X that allows for that?
    # We can brute force it...
    v_y = 75
    v_x = 1
    reached = False
    best_x = None
    for i in range(v_x, 500):
        curr_x = 0
        curr_y = 0
        curr_v_y = v_y
        curr_v_x = i
        while curr_y > y1:
            curr_x += curr_v_x
            curr_y += curr_v_y
            curr_v_y -= 1
            if curr_v_x > 0:
                curr_v_x -= 1
            if curr_v_x < 0:
                curr_v_x += 0
            if y1 <= curr_y <= y2 and \
                    x1 <= curr_x <= x2:
                reached = True
                break
        if reached:
            best_x = i
            break
    if reached:
        print(sum(range(v_y + 1)))
        print(best_x)


def part_2():
    _input = read_file("input.txt")[0]
    x1, x2, y1, y2 = parse_input(_input)

    v_y = -100
    v_x = -100
    init_vs = []
    for i in range(v_x, 2000):
        for j in range(v_y, 100):
            reached = False
            curr_x = 0
            curr_y = 0
            curr_v_x = i
            curr_v_y = j
            while curr_y >= y1:
                curr_x += curr_v_x
                curr_y += curr_v_y
                curr_v_y -= 1
                if curr_v_x > 0:
                    curr_v_x -= 1
                if curr_v_x < 0:
                    curr_v_x += 1
                if y1 <= curr_y <= y2 and \
                        x1 <= curr_x <= x2:
                    reached = True
                    break
            if reached:
                init_vs.append((i, j))
    print(len(init_vs))
    print(len(set(init_vs)))
    print(init_vs)

if __name__ == "__main__":
    part_2()
