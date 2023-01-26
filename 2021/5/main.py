from utils.input import read_file


def parse_line(line):
    pts = line.split(" -> ")
    pt_1 = [int(p) for p in pts[0].split(",")]
    pt_2 = [int(p) for p in pts[1].split(",")]
    return pt_1, pt_2


def part_1():
    lines = read_file("input.txt")
    parsed_lines = [parse_line(line) for line in lines]
    print(parsed_lines[0])
    grid = [[0 for _ in range(1000)] for _ in range(1000)]
    for pt1, pt2 in parsed_lines:
        x1, y1 = pt1
        x2, y2 = pt2
        if pt1[0] != pt2[0] and pt1[1] != pt2[1]:
            continue
        if x1 == x2:
            _min = min(y1, y2)
            _max = max(y1, y2)
            for y in range(_min, _max + 1):
                grid[y][x1] += 1
        elif y1 == y2:
            _min = min(x1, x2)
            _max = max(x1, x2)
            for x in range(_min, _max + 1):
                grid[y1][x] += 1
        else:
            raise ValueError("Help!")
    total = 0
    for i in range(len(grid)):
        for j in range(len(grid[0])):
            if grid[i][j] > 1:
                total += 1
    print(total)
    for i in range(510, 520):
        print(grid[i])


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
    part_2()
