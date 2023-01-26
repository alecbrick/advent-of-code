from utils.input import read_file


def part_1():
    lines = read_file("2.txt")

    total = 0
    for line in lines:
        tokens = line.split()
        range_str = tokens[0]
        char = tokens[1][0]
        password = tokens[2]

        min_max = range_str.split("-")
        min_count = int(min_max[0])
        max_count = int(min_max[1])

        char_count = len([x for x in password if x == char])
        if min_count <= char_count <= max_count:
            total += 1
    print(total)


def part_2():
    lines = read_file("2.txt")

    total = 0
    for line in lines:
        tokens = line.split()
        range_str = tokens[0]
        char = tokens[1][0]
        password = tokens[2]

        min_max = range_str.split("-")
        index_one = int(min_max[0]) - 1
        index_two = int(min_max[1]) - 1

        is_at_index_one = password[index_one] == char
        is_at_index_two = password[index_two] == char

        if (is_at_index_one and not is_at_index_two) or \
                (not is_at_index_one and is_at_index_two):
            total += 1
    print(total)


if __name__ == "__main__":
    part_2()
