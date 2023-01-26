from utils.input import read_file


def parse_line(line):
    command = line.split()
    return command[0], int(command[1])


def find_rating(lines, most_common):
    curr_lines = lines.copy()
    for i in range(len(lines[0])):
        new_lines = []
        counts = [0, 0]
        for l in curr_lines:
            if l[i] == "0":
                counts[0] += 1
            else:
                counts[1] += 1
        if most_common:
            if counts[0] > counts[1]:
                index = 0
            else:
                index = 1
        else:
            if counts[1] < counts[0]:
                index = 1
            else:
                index = 0
        if (counts[1] > counts[0] and most_common) or \
                (counts[1] < counts[0] and not most_common):
            index = 1
        for l in curr_lines:
            if l[i] == str(index):
                new_lines.append(l)
        if len(new_lines) == 1:
            return new_lines[0]
        curr_lines = new_lines
    raise ValueError(f"Curr lines is {curr_lines}")


def part_1():
    lines = read_file("input.txt")
    l = len(lines[0])
    one_counts = [0 for i in range(l)]
    for line in lines:
        for i, c in enumerate(line):
            if c == "1":
                one_counts[i] += 1
    epsilon = ""
    gamma = ""
    print(one_counts)
    for i in one_counts:
        if i > (len(lines) - i):
            epsilon += "1"
            gamma += "0"
        else:
            epsilon += "0"
            gamma += "1"
    print(epsilon)
    print(gamma)
    i_e = int(epsilon, 2)
    i_g = int(gamma, 2)
    print(i_e * i_g)


def part_2():
    lines = read_file("input.txt")
    oxy = find_rating(lines, True)
    carb = find_rating(lines, False)
    print(oxy)
    print(int(oxy, 2))
    print(carb)
    print(int(carb, 2))
    print(int(oxy, 2) * int(carb, 2))

if __name__ == "__main__":
    part_2()
