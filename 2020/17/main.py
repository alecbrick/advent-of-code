from collections import defaultdict

from utils.input import read_file, read_batches


def new_state(w, z, y, x, cube):
    w_list = [w - 1, w, w + 1]
    z_list = [z - 1, z, z + 1]
    y_list = [y - 1, y, y + 1]
    x_list = [x - 1, x, x + 1]
    is_active = x in cube.get(w, {}).get(z, {}).get(y, set())
    total = 0
    for h in w_list:
        for i in z_list:
            for j in y_list:
                for k in x_list:
                    if h == w and i == z and j == y and k == x:
                        continue
                    if k in cube.get(h, {}).get(i, {}).get(j, set()):
                        total += 1
    if is_active:
        if total == 2 or total == 3:
            return True
        else:
            return False
    else:
        if total == 3:
            return True
        else:
            return False


def iterate(cube):
    """
    :param cube: The outer array represents the z-axis. Next is the y-axis, and finally the x-axis.
    This process can expand the size of the cube
    :return:
    """

    new_cube = {}
    layers = cube.keys()
    min_w = min(layers)
    max_w = max(layers)
    min_zs = []
    max_zs = []
    min_ys = []
    max_ys = []
    min_xs = []
    max_xs = []

    for w, mcube in cube.items():
        mcubes = mcube.keys()
        min_zs.append(min(mcubes))
        max_zs.append(max(mcubes))
        for z, layer in mcube.items():
            rows = layer.keys()
            min_ys.append(min(rows))
            max_ys.append(max(rows))
            for y, row in layer.items():
                min_xs.append(min(row))
                max_xs.append(max(row))

    min_z = min(min_zs)
    max_z = max(max_zs)
    min_y = min(min_ys)
    max_y = max(max_ys)
    min_x = min(min_xs)
    max_x = max(max_xs)

    for w in range(min_w - 1, max_w + 2):
        found_z = False
        new_cube[w] = {}
        for z in range(min_z - 1, max_z + 2):
            found_y = False
            new_cube[w][z] = {}
            for y in range(min_y - 1, max_y + 2):
                found_x = False
                new_cube[w][z][y] = set()
                for x in range(min_x - 1, max_x + 2):
                    new = new_state(w, z, y, x, cube)
                    if new:
                        new_cube[w][z][y].add(x)
                        found_x = True
                        found_y = True
                        found_z = True
                if not found_x:
                    del(new_cube[w][z][y])
            if not found_y:
                del(new_cube[w][z])
        if not found_z:
            del(new_cube[w])
    return new_cube


def main():
    lines = read_file("input.txt")
    cube = {0: {0: {}}}
    for i, line in enumerate(lines):
        cube[0][0][i] = set()
        for j, c in enumerate(line):
            if c == "#":
                cube[0][0][i].add(j)

    for i in range(6):
        cube = iterate(cube)

    total = 0
    for w, mcube in cube.items():
        for z, layer in mcube.items():
            for y, row in layer.items():
                total += len(row)

    print(f"Solution: {total}")


if __name__ == "__main__":
    main()
