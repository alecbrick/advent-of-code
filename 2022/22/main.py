import copy
from utils.input import read_file, read_batches


def fix_map(_map):
    """Fixes _map in-place"""
    longest_row = max(len(row) for row in _map)
    for i in range(len(_map)):
        row = _map[i]
        diff = longest_row - len(row)
        if diff > 0:
            row += " " * diff
        _map[i] = row


def get_start(_map):
    print(_map[0])
    return _map[0].index(".")


CARETS = [">", "v", "<", "^"]


def _stitch(y, x, face):
    if y == 0 and 50 <= x < 100 and face == 3:
        t = 1
        ret = x + 100, 0, 0
    elif x == 0 and 150 <= y < 200 and face == 2:
        t = 2
        ret = 0, y - 100, 1
    elif y == 0 and 100 <= x < 150 and face == 3:
        t = 3
        ret = 199, x - 100, 3
    elif y == 199 and 0 <= x < 50 and face == 1:
        t = 4
        ret = 0, x + 100, 1
    elif x == 50 and 0 <= y < 50 and face == 2:
        t = 5
        ret = 100 + (49 - y), 0, 0
    elif x == 0 and 100 <= y < 150 and face == 2:
        t = 6
        ret = 149 - y, 50, 0
    elif x == 149 and 0 <= y < 50 and face == 0:
        t = 7
        ret = 100 + (49 - y), 99, 2
    elif x == 99 and 100 <= y < 150 and face == 0:
        t = 8
        ret = 149 - y, 149, 2
    elif y == 49 and 100 <= x < 150 and face == 1:
        t = 9
        ret = x - 50, 99, 2
    elif x == 99 and 50 <= y < 100 and face == 0:
        t = 10
        ret = 49, y + 50, 3
    elif x == 50 and 50 <= y < 100 and face == 2:
        t = 11
        ret = 100, y - 50, 1
    elif y == 100 and 0 <= x < 50 and face == 3:
        t = 12
        ret = x + 50, 50, 0
    elif y == 149 and 50 <= x < 100 and face == 1:
        t = 13
        ret = 100 + x, 49, 2
    elif x == 49 and 150 <= y < 200 and face == 0:
        t = 14
        ret = 149, y - 100, 3
    else:
        print(y, x)
        raise ValueError
    print(f"Type {t}")
    return ret


def stitch(y, x, face):
    print(f"Stitching on {y}, {x}. Face: {CARETS[face]}")
    new_y, new_x, face = _stitch(y, x, face)
    print(f"Result: {new_y}, {new_x}. Face: {CARETS[face]}")
    return new_y, new_x, face


def parse_steps(steps):
    ret = []
    curr_step = ""
    for c in steps:
        if c == "R" or c == "L":
            ret.append(int(curr_step))
            ret.append(c)
            curr_step = ""
        else:
            curr_step += c
    ret.append(int(curr_step))
    return ret




def take_step_on_map(_map, loc, face, step, marked_map):
    print(loc, face, step)
    new_y, new_x = loc[0], loc[1]
    for i in range(step):
        temp_y, temp_x = new_y, new_x
        caret = CARETS[face]
        marked_map[new_y] = marked_map[new_y][:new_x] + caret + marked_map[new_y][new_x + 1:]
        if face == 0:
            temp_x += 1
            if temp_x >= len(_map[temp_y]) or _map[temp_y][temp_x] == " ":
                temp_x = 0
                while _map[temp_y][temp_x] == " ":
                    temp_x += 1
        elif face == 1:
            temp_y += 1
            if temp_y >= len(_map) or _map[temp_y][temp_x] == " ":
                temp_y = 0
                while _map[temp_y][temp_x] == " ":
                    temp_y += 1
        elif face == 2:
            temp_x -= 1
            if temp_x < 0 or _map[temp_y][temp_x] == " ":
                temp_x = len(_map[temp_y]) - 1
                while _map[temp_y][temp_x] == " ":
                    temp_x -= 1
        else:
            temp_y -= 1
            if temp_y < 0 or _map[temp_y][temp_x] == " ":
                temp_y = len(_map) - 1
                while _map[temp_y][temp_x] == " ":
                    temp_y -= 1
        # Hit a wall?
        if _map[temp_y][temp_x] == "#":
            return [new_y, new_x]
        new_y, new_x = temp_y, temp_x
    return [new_y, new_x]


def take_step_on_map_2(_map, loc, face, step, marked_map):
    print(loc, face, step)
    new_y, new_x = loc[0], loc[1]
    new_face = face
    for i in range(step):
        temp_y, temp_x = new_y, new_x
        caret = CARETS[new_face]
        marked_map[new_y] = marked_map[new_y][:new_x] + caret + marked_map[new_y][new_x + 1:]
        temp_face = new_face
        if new_face == 0:
            temp_x += 1
            if temp_x >= len(_map[temp_y]) or _map[temp_y][temp_x] == " ":
                temp_y, temp_x, temp_face = stitch(new_y, new_x, new_face)
        elif new_face == 1:
            temp_y += 1
            if temp_y >= len(_map) or _map[temp_y][temp_x] == " ":
                temp_y, temp_x, temp_face = stitch(new_y, new_x, new_face)
        elif new_face == 2:
            temp_x -= 1
            if temp_x < 0 or _map[temp_y][temp_x] == " ":
                temp_y, temp_x, temp_face = stitch(new_y, new_x, new_face)
        else:
            temp_y -= 1
            if temp_y < 0 or _map[temp_y][temp_x] == " ":
                temp_y, temp_x, temp_face = stitch(new_y, new_x, new_face)
        # Hit a wall?
        if _map[temp_y][temp_x] == "#":
            if new_face != temp_face:
                print("Nope!")
            return [new_y, new_x], new_face
        new_y, new_x = temp_y, temp_x
        new_face = temp_face
    return [new_y, new_x], new_face


def part_1():
    _map, str_steps = read_batches("input.txt", strip=False)
    fix_map(_map)
    marked_map = copy.deepcopy(_map)
    loc = [0, get_start(_map)]
    print(loc)
    face = 0
    steps = parse_steps(str_steps[0])

    for step in steps:
        if step == "R":
            face = (face + 1) % 4
        elif step == "L":
            face = (face - 1) % 4
        else:
            loc = take_step_on_map(_map, loc, face, step, marked_map)
    with open("marked_map.txt", "w") as f:
        f.writelines([row + "\n" for row in marked_map])
    print(loc)
    print(face)
    print((loc[0] + 1) * 1000 + (loc[1] + 1) * 4 + face)


def part_2():
    _map, str_steps = read_batches("input.txt", strip=False)
    fix_map(_map)
    marked_map = copy.deepcopy(_map)
    loc = [0, get_start(_map)]
    print(loc)
    face = 0
    steps = parse_steps(str_steps[0])

    i = 0
    for step in steps:
        if step == "R":
            face = (face + 1) % 4
        elif step == "L":
            face = (face - 1) % 4
        else:
            loc, face = take_step_on_map_2(_map, loc, face, step, marked_map)
        i += 1
    with open("marked_map.txt", "w") as f:
        f.writelines([row + "\n" for row in marked_map])
    print(loc)
    print(face)
    print((loc[0] + 1) * 1000 + (loc[1] + 1) * 4 + face)


if __name__ == "__main__":
    part_2()
