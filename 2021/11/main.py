from collections import defaultdict

from utils.input import read_file


def parse_lines(lines):
    ret = []
    for line in lines:
        r = []
        for c in line:
            r.append(int(c))
        ret.append(r)
    return ret


def step(grid):
    q = []
    visited = set()
    flashes = 0
    for i in range(len(grid)):
        for j in range(len(grid[0])):
            grid[i][j] += 1
            if grid[i][j] > 9:
                q.append((i, j))
    while len(q) > 0:
        i, j = q.pop(0)
        if (i, j) in visited:
            continue
        visited.add((i, j))
        flashes += 1
        for a in [-1, 0, 1]:
            for b in [-1, 0, 1]:
                if a == 0 and b == 0:
                    continue
                x = i + a
                y = j + b
                if x < 0 or y < 0 or x >= len(grid) or y >= len(grid[0]):
                    continue
                grid[x][y] += 1
                if grid[x][y] > 9:
                    q.append((x, y))
    for i in range(len(grid)):
        for j in range(len(grid[0])):
            if grid[i][j] > 9:
                grid[i][j] = 0
    return flashes


def part_1():
    lines = read_file("input.txt")
    grid = parse_lines(lines)
    total_flashes = 0
    for i in range(100):
        num_flashes = step(grid)
        total_flashes += num_flashes
    print(total_flashes)


def part_2():
    lines = read_file("input.txt")
    grid = parse_lines(lines)
    total_flashes = 0
    for i in range(1000):
        num_flashes = step(grid)
        total_flashes += num_flashes
        if num_flashes == 100:
            print(i + 1)
    print(total_flashes)


if __name__ == "__main__":
    part_1()
