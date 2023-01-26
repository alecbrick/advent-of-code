from collections import defaultdict

from utils.input import read_file


def parse_line(line):
    pts = line.split(" -> ")
    pt_1 = [int(p) for p in pts[0].split(",")]
    pt_2 = [int(p) for p in pts[1].split(",")]
    return pt_1, pt_2


def triangle(n):
    return sum(range(1, n + 1))


def fuel(nums, dest):
    return sum([triangle(abs(num - dest)) for num in nums])


def find_best_pos(nums):
    best = 0
    for i in range(max(nums)):
        fuel_used = fuel(nums, i)
        if best == 0 or fuel_used < best:
            best = fuel_used
    return best


def part_1():
    lines = read_file("input.txt")
    nums = [int(n) for n in lines[0].split(",")]
    best = find_best_pos(nums)
    print(best)


def part_2():
    lines = read_file("input.txt")
    parsed_lines = [parse_line(line) for line in lines]
    print(parsed_lines[0])
    grid = [[0 for _ in range(1000)] for _ in range(1000)]
    for pt1, pt2 in parsed_lines:
        x1, y1 = pt1
        x2, y2 = pt2
        min_x = min(x1, x2)
        max_x = max(x1, x2)
        min_y = min(y1, y2)
        max_y = max(y1, y2)
        diff_x = max_x - min_x
        diff_y = max_y - min_y
        if not (x1 == x2 or y1 == y2 or diff_x == diff_y):
            continue
        curr_x = x1
        curr_y = y1
        signed_x = x2 - x1
        signed_y = y2 - y1
        while True:
            grid[curr_x][curr_y] += 1
            if curr_x == x2 and curr_y == y2:
                break
            if signed_x > 0:
                curr_x += 1
            elif signed_x < 0:
                curr_x -= 1
            if signed_y > 0:
                curr_y += 1
            elif signed_y < 0:
                curr_y -= 1
    total = 0
    for i in range(len(grid)):
        for j in range(len(grid[0])):
            if grid[i][j] > 1:
                total += 1
    print(total)
    for i in range(50, 60):
        print(grid[i])


if __name__ == "__main__":
    part_1()
