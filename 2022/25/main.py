import copy
from collections import defaultdict
from dataclasses import dataclass, field
from queue import PriorityQueue
from typing import Any

from utils.input import read_file, read_batches


def part_1():
    lines = read_file("input.txt")
    full_count = 0
    for line in lines:
        rev_line = reversed(line)
        mul = 1
        total = 0
        for c in rev_line:
            if c == "=":
                total += (-2 * mul)
            elif c == "-":
                total += (-1 * mul)
            else:
                total += int(c) * mul
            mul *= 5
        full_count += total

    root = 1
    while 5**root < full_count:
        root += 1
    print(full_count)
    print(root)

    max_num = sum(10 * 5**i for i in range(root))
    print(max_num)
    if max_num < full_count:
        root -= 1

    snafu_num = ""
    curr_num = 0
    target = full_count
    while root >= 0:
        # For each position of the snafu number:
        # - If our current number is _less_ than the target, add 1 or 2.
        # - If we go over, that's fine! But only to a certain extent.
        # - Specifically, if we add the max_num to our current, and it's _greater_ than
        #   the target, that's good, it's in range of the rest of the digits.
        print(f"New root: {root}")
        print(f"Target: {target}")
        print(f"Current number: {curr_num}")
        next_max = sum(10 * 5 ** i for i in range(root - 1)) if root > 0 else 0
        print(f"Max of next root: {next_max}")
        if curr_num <= target <= curr_num + next_max:
            snafu_num += "0"
        elif curr_num + next_max < target <= curr_num + 5 ** root + next_max:
            snafu_num += "1"
            curr_num += 5 ** root
        elif curr_num + next_max + 5 ** root < target <= curr_num + 2 * (5**root) + next_max:
            snafu_num += "2"
            curr_num += 2*(5**root)
        elif curr_num - (5**root) - next_max <= target < curr_num:
            snafu_num += "-"
            curr_num -= 5**root
        elif curr_num - 2*(5**root) - next_max <= target < curr_num - (5**root) - next_max:
            snafu_num += "="
            curr_num -= 2*(5**root)
        else:
            raise ValueError(f"aaaa {root} {snafu_num} {curr_num} {target}" )
        root -= 1
    print(snafu_num)


def part_2():
    lines = read_file("input.txt")
    full_count = 0
    mapping = {
        "=": -2,
        "-": -1,
        "0": 0,
        "1": 1,
        "2": 2,
    }
    for line in lines:
        rev_line = reversed(line)
        mul = 1
        total = 0
        for c in rev_line:
            total += mapping[c] * mul
            mul *= 5
        full_count += total

    rev_mapping = {v: k for k, v in mapping.items()}
    snafu_num = ""
    curr_num = full_count
    while curr_num > 0:
        mod = curr_num % 5
        for v, k in rev_mapping.items():
            if (v % 5) == mod:
                snafu_num += k
                curr_num -= v
                curr_num /= 5
                break
    print(''.join(reversed(snafu_num)))


if __name__ == "__main__":
    part_2()
