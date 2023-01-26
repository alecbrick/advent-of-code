from utils.input import read_file


def read_insts(lines):
    ret = []
    for line in lines:
        pair = line.split(" = ")
        ret.append(pair)
    return ret


def run_insts_1(insts):
    mask = {}
    output = {}
    for inst in insts:
        left = inst[0]
        right = inst[1]
        if left == "mask":
            mask = {}
            for i in range(len(right)):
                char = right[-(i + 1)]
                if char != "X":
                    digit = 2 ** i
                    mask_val = int(char)
                    mask[digit] = mask_val
        else:
            addr = int(left[4:-1])
            val = int(right)
            for mask_digit, mask_val in mask.items():
                mod = val % (mask_digit * 2)
                is_zero = mod < mask_digit
                if is_zero and mask_val == 1:
                    val += mask_digit
                elif not is_zero and mask_val == 0:
                    val -= mask_digit
            output[addr] = val
    return output


def all_addrs(addr, x_digits):
    if len(x_digits) == 0:
        return [addr]
    x_digit = x_digits[0]
    one_addr = addr | x_digit
    zero_addr = addr & ~x_digit
    return all_addrs(one_addr, x_digits[1:]) + all_addrs(zero_addr, x_digits[1:])


def run_insts_2(insts):
    mask = {}
    output = {}
    for inst in insts:
        left = inst[0]
        right = inst[1]
        if left == "mask":
            mask = {}
            for i in range(len(right)):
                char = right[-(i + 1)]
                digit = 2 ** i
                if char != "X":
                    mask_val = int(char)
                    mask[digit] = mask_val
                else:
                    mask[digit] = "X"
        else:
            addr = int(left[4:-1])
            val = int(right)

            x_digits = []
            for mask_digit, mask_val in mask.items():
                if mask_val == 1:
                    addr = addr | mask_digit
                elif mask_val == "X":
                    x_digits.append(mask_digit)
            addrs = all_addrs(addr, x_digits)
            for a in addrs:
                output[a] = val
    return output


def main():
    lines = read_file("input.txt")
    insts = read_insts(lines)

    output = run_insts_2(insts)
    print(f"Solution: {sum(output.values())}")


if __name__ == "__main__":
    main()
