from utils.input import read_file


def parse_input(lines):
    ret = []
    for line in lines:
        on = False
        parts = line.split()
        if parts[0] == "on":
            on = True
        xyz = parts[1].split(",")
        xyzs = []
        for x in xyz:
            ab = x.split("=")[1].split("..")
            ij = [int(ab[0]), int(ab[1])]
            xyzs.append(ij)
        ret.append((on, xyzs))
    return ret


def get_overlap(cube_1, cube_2):
    """
    (1, 5) (2, 4) => (2, 4)
    (1, 5) (3, 8) => (3, 5)

    :param cube_1: [[x1, x2], [y1, y2], [z1, z2]]
    :param cube_2: [[x1, x2], [y1, y2], [z1, z2]]
    :return: The cube of overlap between the two, or None.
    """
    overlap = []
    for i in range(3):
        b_1 = cube_1[i]
        b_2 = cube_2[i]
        max_a = max([b_1[0], b_2[0]])
        min_b = min([b_1[1], b_2[1]])
        if max_a <= min_b:
            o = [max_a, min_b]
        else:
            o = None
        overlap.append(o)
    if None in overlap:
        return None
    return overlap


def contains(cube1, cube2):
    for i in range(3):
        if cube2[i][0] < cube1[i][0]:
            return False
        if cube2[i][1] > cube1[i][1]:
            return False
    return True


def update_cuboids(cuboids, line):
    inst = line[0]
    new_cube = line[1]
    new_cuboids = []
    if len(cuboids) == 0 and inst:
        new_cuboids.append(new_cube)
        return new_cuboids
    for cube in cuboids:
        overlap = get_overlap(new_cube, cube)
        if overlap is None:
            # No change
            new_cuboids.append(cube)
            continue
        if contains(new_cube, cube):
            # If new cube contains old cube, then just get rid of old cube entirely.
            continue
        # We break "cube" into 8 or 27 pieces. We then add the 7 or 26 cubes that aren't the overlap.
        ranges = []
        for i in range(3):
            to_append = []
            if cube[i][0] < overlap[i][0]:
                to_append.append([cube[i][0], overlap[i][0] - 1])
            to_append.append(overlap[i])
            if overlap[i][1] < cube[i][1]:
                to_append.append([overlap[i][1] + 1, cube[i][1]])
            ranges.append(to_append)

        for x in ranges[0]:
            for y in ranges[1]:
                for z in ranges[2]:
                    lil_cube = [x, y, z]
                    if lil_cube == overlap:
                        continue
                    new_cuboids.append(lil_cube)

    if inst:
        new_cuboids.append(new_cube)
    return new_cuboids


def count_cuboids(cuboids):
    total = 0
    for cube in cuboids:
        cube_size = 1
        for edge in cube:
            cube_size *= edge[1] - edge[0] + 1
        total += cube_size
    return total


def part_1():
    lines = read_file("input.txt")
    lines = parse_input(lines)
    print(lines)

    """
    Hmm.
    I think my strategy should be as follows.
    We should keep track of everything that's on in terms of _cubes_.
    If we turn _off_ something that intersects with something _on_,
    then we break the _on_ pieces into smaller cuboids.
    """
    cuboids = []
    for line in lines:
        cuboids = update_cuboids(cuboids, line)
    count = count_cuboids(cuboids)
    print(count)


if __name__ == "__main__":
    part_1()
