from utils.input import read_file


def parse_num(num):
    if num[0] == "+":
        return int(num[1:])
    return -int(num[1:])


def parse_instructions(lines):
    pairs = [line.split(" ") for line in lines]
    pairs = [(pair[0], parse_num(pair[1])) for pair in pairs]
    return pairs


def part_1(lines):
    insts = parse_instructions(lines)
    seen = set()
    i = 0
    acc = 0
    while True:
        print(insts[i])
        print(i)
        print(acc)
        if i in seen:
            print(acc)
            break
        seen.add(i)
        inst = insts[i]
        fun = inst[0]
        val = inst[1]
        if fun == "acc":
            acc += val
            i += 1
        elif fun == "jmp":
            i += val
        elif fun == "nop":
            i += 1
        else:
            raise ValueError(f"What to heck! {inst}")


def run_program(insts):
    acc = 0
    i = 0
    seen = set()
    while i < len(insts):
        if i in seen:
            print(f"Infinite loop at line: {insts[i]}")
            raise Exception("Infinite loop!")
        seen.add(i)
        inst = insts[i]
        fun = inst[0]
        val = inst[1]
        if fun == "acc":
            acc += val
            i += 1
        elif fun == "jmp":
            i += val
        elif fun == "nop":
            i += 1
        else:
            raise ValueError(f"What to heck! {inst}")
    return acc


def part_2(lines):
    insts = parse_instructions(lines)

    for i in range(len(insts)):
        inst = insts[i]
        print(f"Attempt #{i}: trying {inst}")
        if inst[0] == "acc":
            continue
        insts_copy = insts.copy()
        inst_copy = insts_copy[i]
        if inst_copy[0] == "jmp":
            insts_copy[i] = ("nop", inst_copy[1])
        else:
            insts_copy[i] = ("jmp", inst_copy[1])
        try:
            res = run_program(insts_copy)
            print(f"Solved! {res}")
            return
        except Exception:
            continue


def main():
    lines = read_file("8.txt")
    part_2(lines)


if __name__ == "__main__":
    main()
