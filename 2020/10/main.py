from utils.input import read_file


def part_1(lines):
    sorted_lines = sorted(lines)
    last = 0
    num_1 = 0
    num_3 = 0
    for i in sorted_lines:
        print(f"{i}, {last}")
        if i - last == 1:
            num_1 += 1
        elif i - last == 3:
            num_3 += 1
        last = i
    num_3 += 1
    print(f"{num_1}, {num_3}")
    print(num_1 * num_3)


def part_2(lines):
    lines = sorted(lines)
    totals = {0: 1}
    for i in lines:
        total = 0
        for j in [i - 3, i - 2, i - 1]:
            if totals.get(j):
                total += totals[j]
        totals[i] = total
    print(totals)
    print(totals[lines[-1]])


def main():
    lines = read_file("10.txt")
    lines = [int(line) for line in lines]
    print(sorted(lines))
    part_2(lines)


if __name__ == "__main__":
    main()
