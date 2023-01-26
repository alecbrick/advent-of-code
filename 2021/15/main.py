import math
import heapq

from utils.input import read_file


def parse_input(lines):
    ret = []
    for line in lines:
        l = []
        for c in line:
            l.append(int(c))
        ret.append(l)
    return ret


def part_1():
    lines = read_file("input.txt")
    grid = parse_input(lines)
    dyn_grid = [
        [0 for i in range(len(grid[0]))]
        for _ in range(len(grid))
    ]
    print(grid)
    print(dyn_grid)
    for i in range(len(grid)):
        for j in range(len(grid[0])):
            if i == 0 and j == 0:
                dyn_grid[i][j] = 0
            elif i == 0:
                dyn_grid[i][j] = grid[i][j] + dyn_grid[i][j - 1]
            elif j == 0:
                dyn_grid[i][j] = grid[i][j] + dyn_grid[i - 1][j]
            else:
                _min = min(dyn_grid[i - 1][j], dyn_grid[i][j - 1])
                dyn_grid[i][j] = grid[i][j] + _min
    print(dyn_grid[-1][-1])


def part_2():
    lines = read_file("input.txt")
    grid = parse_input(lines)
    in_queue = [
        [True for i in range(len(grid[0]) * 5)]
        for _ in range(len(grid) * 5)
    ]
    dyn_grid = [
        [Vertex(i, j, math.inf) for j in range(len(grid[0]) * 5)]
        for i in range(len(grid) * 5)
    ]
    q = [(math.inf, i, j) for i in range(len(dyn_grid)) for j in range((len(dyn_grid[0])))]
    q[0] = (0, 0, 0)
    print(q[:10])
    heapq.heapify(q)

    while len(q) > 0:
        min_q = heapq.heappop(q)
        i, j = min_q[1], min_q[2]
        if not in_queue[i][j]:
            continue
        in_queue[i][j] = False
        neighbors = [[i - 1, j], [i + 1, j], [i, j - 1], [i, j + 1]]
        for a, b in neighbors:
            if a < 0 or b < 0 or a >= len(dyn_grid) or b >= len(dyn_grid[0]):
                continue
            grid_i = a % len(grid)
            grid_j = b % len(grid[0])
            i_modifier = a // len(grid)
            j_modifier = b // len(grid[0])
            mod = i_modifier + j_modifier
            grid_spot = (grid[grid_i][grid_j] + mod)
            if grid_spot > 9:
                grid_spot -= 9
            heapq.heappush(q, (min_q[0] + grid_spot, a, b))
        if i == len(dyn_grid) - 1 and j == len(dyn_grid[0]) - 1:
            print(min_q[0])
            return


if __name__ == "__main__":
    part_2()
