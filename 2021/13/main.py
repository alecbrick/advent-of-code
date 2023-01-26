from collections import defaultdict

from utils.input import read_file, read_batches


def parse_dots(dots):
    ret = []
    for d in dots:
        a = d.split(",")
        ret.append([int(a[0]), int(a[1])])
    return ret


def plot_dots(dots):
    max_x = max(d[0] for d in dots)
    max_y = max(d[1] for d in dots)
    grid = [["." for _ in range(max_x + 1)] for _ in range(max_y + 1)]
    for d in dots:
        grid[d[1]][d[0]] = "#"
    return grid


def fold_grid(grid, axis, n):
    if axis == "y":
        bottom_height = len(grid) - n - 1
    elif axis == "x":
        bottom_height = len(grid[0]) - n - 1
    else:
        raise ValueError(axis)
    new_size = max(n, bottom_height)
    if axis == "y":
        ret = [[grid[i][j] for j in range(len(grid[0]))] for i in range(new_size)]
    else:
        ret = [[grid[i][j] for j in range(new_size)] for i in range(len(grid))]
    if axis == "y":
        for i in range(n + 1, len(grid)):
            for j in range(len(grid[0])):
                if grid[i][j] == "#":
                    diff = i - (i - n) * 2
                    ret[diff][j] = "#"
    else:
        for i in range(len(grid)):
            for j in range(n + 1, len(grid[0])):
                if grid[i][j] == "#":
                    diff = j - (j - n) * 2
                    ret[i][diff] = "#"

    return ret


def part_1():
    batches = read_batches("input.txt")
    dots = parse_dots(batches[0])
    insts = batches[1]

    grid = plot_dots(dots)
    print(grid)

    for inst in insts:
        a_n = inst.split(" ")[2]
        a, n = a_n.split("=")
        new_grid = fold_grid(grid, a, int(n))
        grid = new_grid
    print(grid)


if __name__ == "__main__":
    part_1()
