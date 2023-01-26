from utils.input import read_file


def parse_input(lines):
    ret = []
    for line in lines:
        if len(line) == 0:
            return ret
        s = line.split()
        args = s[1:]
        args = [int(c) if (c.isnumeric() or c[0] == "-" and c[1:].isnumeric()) else c for c in args]
        ret.append((s[0], args))
    return ret


def get_value(arg, values):
    if isinstance(arg, int):
        return arg
    return values[arg]


def run_program(insts, inps=None):
    values = {
        "w": 0,
        "x": 0,
        "y": 0,
        "z": 0,
    }
    inp_count = 0
    for inst, args in insts:
        if inst == "inp":
            if inps is not None:
                values[args[0]] = inps[inp_count]
                inp_count += 1
            else:
                x = input(f"Please input a value for {args[0]}:")
                values[args[0]] = int(x)
        elif inst == "add":
            s = values[args[0]] + get_value(args[1], values)
            values[args[0]] = s
        elif inst == "mod":
            s = values[args[0]] % get_value(args[1], values)
            values[args[0]] = s
        elif inst == "div":
            s = values[args[0]] // get_value(args[1], values)
            values[args[0]] = s
        elif inst == "mul":
            s = values[args[0]] * get_value(args[1], values)
            values[args[0]] = s
        elif inst == "eql":
            if values[args[0]] == get_value(args[1], values):
                values[args[0]] = 1
            else:
                values[args[0]] = 0
    return values


def part_1():
    lines = read_file("input.txt")
    insts = parse_input(lines)
    inps = [7, 4, 9, 2, 9, 9, 9, 5, 9, 9, 9, 3, 8, 9]
    values = run_program(insts, inps)
    print(values)
    # 74929995999389

# 1 2 3 4 3 2 3 2 1 0 1 0 1 0
def part_2():
    lines = read_file("input.txt")
    insts = parse_input(lines)
    inps = [1, 1, 1, 1, 8, 1, 5, 1, 6, 3, 7, 1, 1, 2]
    values = run_program(insts, inps)
    print(values)
    # 11118151637112


if __name__ == "__main__":
    part_2()
