from utils.input import read_file


PREAMBLE_LEN = 25


def valid_numbers(nums):
    ret = set()
    for i in range(len(nums) - 1):
        for j in range(i + 1, len(nums)):
            ret.add(int(nums[i]) + int(nums[j]))
    return ret


def part_1(preamble, rest):
    while True:
        sum_dict = valid_numbers(preamble)
        print(sum_dict)
        if int(rest[0]) not in sum_dict:
            return int(rest[0])
        preamble = preamble[1:]
        preamble.append(rest[0])
        rest = rest[1:]


def part_2(lines, val):
    lines = [int(line) for line in lines]
    i = 0
    j = 1
    while True:
        rng = lines[i:j + 1]
        total = sum(rng)
        if total == val:
            print(f"Found! {i}, {j}")
            mini = min(rng)
            maxi = max(rng)
            print(f"Answer: {mini + maxi}")
            return
        elif total < val:
            j += 1
        else:
            i += 1


def main():
    lines = read_file("9.txt")
    preamble = lines[:PREAMBLE_LEN]
    rest = lines[PREAMBLE_LEN:]
    val = part_1(preamble, rest)

    part_2(lines, val)


if __name__ == "__main__":
    main()
