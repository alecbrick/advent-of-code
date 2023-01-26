from utils.input import read_file


def part_1():
    lines = read_file("3.txt")

    total = 0
    col = 0
    for i, line in enumerate(lines):
        if i % 2 == 1:
            continue
        if line[col] == "#":
            total += 1
        col += 1
        col %= len(line)
    print(total)


if __name__ == "__main__":
    part_1()

# 67
# 211
# 77
# 89
# 37
