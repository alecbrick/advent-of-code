from utils.input import read_file


def identify_tile(line):
    curr = [0, 0]
    i = 0
    while i < len(line):
        inst_1 = line[i]
        i += 1
        if inst_1 == "e":
            curr[0] += 1
            continue
        elif inst_1 == "w":
            curr[0] -= 1
            continue

        # north or south
        inst_2 = line[i]
        i += 1
        if inst_1 == "n" and inst_2 == "w":
            curr[1] += 1
        elif inst_1 == "n" and inst_2 == "e":
            curr[0] += 1
            curr[1] += 1
        elif inst_1 == "s" and inst_2 == "w":
            curr[0] -= 1
            curr[1] -= 1
        elif inst_1 == "s" and inst_2 == "e":
            curr[1] -= 1
        else:
            raise ValueError("What to heck!")
    return curr


def conway(tiles):
    ret = {}
    black_tiles = [k for k, v in tiles.items() if v]
    min_x = min(t[0] for t in black_tiles)
    max_x = max(t[0] for t in black_tiles)
    min_y = min(t[1] for t in black_tiles)
    max_y = max(t[1] for t in black_tiles)
    for x in range(min_x - 1, max_x + 2):
        for y in range(min_y - 1, max_y + 2):
            adjacent = [
                (x - 1, y),
                (x + 1, y),
                (x, y + 1),
                (x + 1, y + 1),
                (x - 1, y - 1),
                (x, y - 1)
            ]
            total = 0
            for a in adjacent:
                if tiles.get(a, False):
                    total += 1
            point = (x, y)
            if tiles.get(point, False):
                if total == 0 or total > 2:
                    ret[point] = False
                else:
                    ret[point] = True
            else:
                if total == 2:
                    ret[point] = True
                else:
                    ret[point] = False
    return ret


def main():
    lines = read_file("input.txt")
    tiles = {}
    for line in lines:
        pos = tuple(identify_tile(line))
        if pos in tiles:
            tiles[pos] = not tiles[pos]
        else:
            tiles[pos] = True
    for i in range(100):
        tiles = conway(tiles)
    print(len([v for v in tiles.values() if v]))


if __name__ == "__main__":
    main()
