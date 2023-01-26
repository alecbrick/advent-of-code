from utils.input import read_file


def parse_line(line):
    command = line.split()
    return command[0], int(command[1])


def part_1():
    lines = read_file("input.txt")
    commands = [parse_line(line) for line in lines]
    position = [0, 0]
    for command in commands:
        if command[0] == "forward":
            position[0] += command[1]
        elif command[0] == "down":
            position[1] += command[1]
        elif command[0] == "up":
            position[1] -= command[1]
        print(position)
    print(position[0] * position[1])


def part_2():
    lines = read_file("input.txt")
    commands = [parse_line(line) for line in lines]
    position = [0, 0]
    aim = 0
    for command in commands:
        if command[0] == "forward":
            position[0] += command[1]
            position[1] += command[1] * aim
        elif command[0] == "down":
            aim += command[1]
        elif command[0] == "up":
            aim -= command[1]
        print(position)
    print(position[0] * position[1])


if __name__ == "__main__":
    part_2()
