from utils.input import read_file, read_batches


def part_1():
    lines = read_file("input.txt")
    total = 0
    for line in lines:
        mid_line = len(line) // 2
        left = line[:mid_line]
        right = line[mid_line:]
        in_both = list(set(left).intersection(set(right)))[0]
        if ord(in_both) < 96:
            value = ord(in_both) - 64 + 26
        else:
            value = ord(in_both) - 96
        total += value
    print(total)


def part_2():
    lines = read_file("input.txt")
    total = 0
    i = 0
    while i < len(lines):
        left = lines[i]
        mid = lines[i + 1]
        right = lines[i + 2]
        in_both = list(set(left).intersection(set(mid)).intersection(set(right)))[0]
        if ord(in_both) < 96:
            value = ord(in_both) - 64 + 26
        else:
            value = ord(in_both) - 96
        total += value
        i += 3
    print(total)


if __name__ == "__main__":
    part_2()
