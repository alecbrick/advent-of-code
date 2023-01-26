from collections import defaultdict

from utils.input import read_file



def parse_line(line):
    pts = line.split(" | ")
    signals = pts[0].split(" ")
    output = pts[1].split(" ")
    return signals, output


def part_1():
    lines = read_file("input.txt")
    rows = [[int(c) for c in row] for row in lines]
    print(rows)
    found_points = []

    for i in range(len(rows)):
        for j in range(len(rows[i])):
            curr = rows[i][j]
            found = False
            for x, y in [(i - 1, j), (i + 1, j), (i, j - 1), (i, j + 1)]:
                if x < 0 or y < 0 or x >= len(rows) or y >= len(rows[0]):
                    continue
                try:
                    val = rows[x][y]
                    if val <= curr:
                        found = True
                except IndexError:
                    pass
            if not found:
                found_points.append((i, j))
    print(found_points)
    total = 0
    for i, j in found_points:
        total += rows[i][j] + 1
    print(total)


def dfs(rows, i, j, visited):
    if (i, j) in visited:
        return []
    if i < 0 or j < 0 or i >= len(rows) or j >= len(rows[0]):
        return []
    if rows[i][j] == 9:
        return []
    visited.append((i, j))
    up = dfs(rows, i - 1, j, visited)
    down = dfs(rows, i + 1, j, visited)
    left = dfs(rows, i, j - 1, visited)
    right = dfs(rows, i, j + 1, visited)
    return [(i, j)] + up + down + left + right


def part_2():
    lines = read_file("input.txt")
    rows = [[int(c) for c in row] for row in lines]
    print(rows)
    found_points = []

    for i in range(len(rows)):
        for j in range(len(rows[i])):
            curr = rows[i][j]
            found = False
            for x, y in [(i - 1, j), (i + 1, j), (i, j - 1), (i, j + 1)]:
                if x < 0 or y < 0 or x >= len(rows) or y >= len(rows[0]):
                    continue
                try:
                    val = rows[x][y]
                    if val <= curr:
                        found = True
                except IndexError:
                    pass
            if not found:
                found_points.append((i, j))
    basin_sizes = []
    for i, j in found_points:
        basin = dfs(rows, i, j, [])
        print(basin)
        basin_size = len(basin)
        basin_sizes.append(basin_size)
    s = sorted(basin_sizes, reverse=True)
    print(s[0] * s[1] * s[2])


if __name__ == "__main__":
    part_2()
