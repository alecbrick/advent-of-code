from collections import defaultdict

from utils.input import read_file


len_to_num = {
    2: [1],
    3: [7],
    4: [4],
    5: [2, 3, 5],
    6: [6, 9, 0],
    7: [8]
}

num_to_letters = {
    0: "abcefg",
    1: "cf",
    2: "acdeg",
    3: "acdfg",
    4: "bcdf",
    5: "abdfg",
    6: "abdefg",
    7: "acf",
    8: "abcdefg",
    9: "abcdfg"
}

reverse_num_to_letters = {
    "abcefg": 0,
    "cf": 1,
    "acdeg": 2,
    "acdfg": 3,
    "bcdf": 4,
    "abdfg": 5,
    "abdefg": 6,
    "acf": 7,
    "abcdefg": 8,
    "abcdfg": 9
}


def parse_line(line):
    pts = line.split(" | ")
    signals = pts[0].split(" ")
    output = pts[1].split(" ")
    return signals, output


def part_1():
    lines = read_file("input.txt")
    lines = [parse_line(line) for line in lines]
    total = 0
    for signals, output in lines:
        for num in output:
            possible_nums = len_to_num[len(num)]
            if len(possible_nums) == 1:
                total += 1

    print(total)


def part_2():
    lines = read_file("input.txt")
    lines = [parse_line(line) for line in lines]
    total = 0
    for signals, output in lines:
        a_to_g = {"a", "b", "c", "d", "e", "f", "g"}
        possibilities = {
            x: a_to_g.copy() for x in a_to_g
        }
        for num in signals:
            possible_nums = len_to_num[len(num)]
            if len(possible_nums) == 1:
                real_letters = num_to_letters[possible_nums[0]]
                for c in a_to_g:
                    possible_c = possibilities[c].copy()
                    c_in_real = c in real_letters
                    for p in possible_c:
                        if c_in_real and p not in num:
                            possibilities[c].discard(p)
                        elif not c_in_real and p in num:
                            possibilities[c].discard(p)
        # At this point, we know what "a" is.
        # (g, e), (b, d), and (c, f) are ambiguous pairs.
        # Now, we look at numbers with 6 segments.
        # This isolates d (in 0), e (in 9), and c (in 6).
        # Specifically, those values are _missing_.
        # For example, say we've narrowed "d" and "b" to "a" and "f".
        # We find a 6-segment number that's missing only "f".
        # So the 6-segment number is missing either "b" or "d".
        # But no 6-segment number can possibly be missing "b", so
        # it must be missing "d".
        # That means it's a 0, and "d" corresponds to "f",
        # while "b" corresponds to "a".
        for num in signals:
            if len(num) != 6:
                continue
            missing_letter = list(set("abcdefg") - set(num))[0]
            for c in "bcdefg":
                if missing_letter not in possibilities[c]:
                    continue
                other_letter = ""
                for p in possibilities[c]:
                    if p != missing_letter:
                        other_letter = p
                        break
                if c in "cde":
                    possibilities[c].discard(other_letter)
                else:
                    possibilities[c].discard(missing_letter)
        # Possibilities are complete. Let's construct the reverse map.
        reverse_map = {}
        for real, fake in possibilities.items():
            reverse_map[list(fake)[0]] = real
        the_number = 0
        for o in output:
            the_number *= 10
            translated_number = ''.join(sorted([reverse_map[c] for c in o]))
            real_number = reverse_num_to_letters[translated_number]
            the_number += real_number
        total += the_number
    print(total)


if __name__ == "__main__":
    part_2()
