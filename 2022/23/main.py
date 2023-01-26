import copy
from collections import defaultdict

from utils.input import read_file, read_batches


def elf_locations(lines):
    locs = []
    for i in range(len(lines)):
        for j in range(len(lines[i])):
            if lines[i][j] == "#":
                locs.append((i, j))
    return locs


def part_1():
    lines = read_file("input.txt")
    locs = set(elf_locations(lines))
    print(locs)
    order = ["N", "S", "W", "E"]
    i = 1
    while True:
        new_locs = set()
        temp_locs = defaultdict(list)
        for loc in locs:
            y, x = loc
            found_elf = False
            for a in [-1, 0, 1]:
                for b in [-1, 0, 1]:
                    if a == 0 and b == 0:
                        continue
                    if (y + a, x + b) in locs:
                        found_elf = True
            if not found_elf:
                new_locs.add(loc)
                continue

            order_found = False
            for o in order:
                if o == "N":
                    to_check = [(y - 1, x - 1), (y - 1, x), (y - 1, x + 1)]
                elif o == "S":
                    to_check = [(y + 1, x - 1), (y + 1, x), (y + 1, x + 1)]
                elif o == "W":
                    to_check = [(y - 1, x - 1), (y, x - 1), (y + 1, x - 1)]
                else:
                    to_check = [(y - 1, x + 1), (y, x + 1), (y + 1, x + 1)]
                new_pos = to_check[1]
                found = False
                for c in to_check:
                    if c in locs:
                        found = True
                        break
                if not found:
                    temp_locs[new_pos].append((y, x))
                    order_found = True
                    break
            if not order_found:
                new_locs.add(loc)
        for new_loc, old_locs in temp_locs.items():
            if len(old_locs) > 1:
                new_locs.update(set(old_locs))
            else:
                new_locs.add(new_loc)
        if locs == new_locs:
            print(f"Complete! i={i}")
            break
        else:
            print(f"Incomplete. i={i}")
        i += 1
        locs = new_locs
        order = order[1:] + [order[0]]

    ys = [loc[0] for loc in locs]
    xs = [loc[1] for loc in locs]
    height = max(ys) - min(ys) + 1
    width = max(xs) - min(xs) + 1
    print((height * width) - len(locs))


def part_2():
    lines = read_file("input.txt")


if __name__ == "__main__":
    part_1()
