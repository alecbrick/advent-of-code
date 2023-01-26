import itertools
from collections import defaultdict

from utils.input import read_file, read_batches


def flip(grid):
    return list(reversed(grid))


def rotate(grid):
    ret = []
    for i in range(len(grid[0])):
        ret_row = []
        for j in range(len(grid) - 1, -1, -1):
            ret_row.append(grid[j][i])
        ret.append(ret_row)
    return ret


def parse_batches(batches):
    ret = {}
    for batch in batches:
        tile_line = batch[0]
        tile = int(tile_line.split()[1][:-1])
        grid = [list(line) for line in batch[1:]]

        rots = []
        rots.append(grid)
        rotated_grid = grid
        for i in range(3):
            rotated_grid = rotate(rotated_grid)
            rots.append(rotated_grid)

        flipped_grid = flip(grid)
        rots.append(flipped_grid)
        for i in range(3):
            flipped_grid = rotate(flipped_grid)
            rots.append(flipped_grid)

        ret[tile] = rots
    return ret


def check_top(grid_1, grid_2):
    return grid_1[0] == grid_2[-1]


def check_bottom(grid_1, grid_2):
    return check_top(grid_2, grid_1)


def check_right(grid_1, grid_2):
    right = [row[-1] for row in grid_1]
    left = [row[0] for row in grid_2]
    return right == left


def check_left(grid_1, grid_2):
    return check_right(grid_2, grid_1)


def reconstruct(grids):
    tiles = list(grids.keys())
    first_tile = tiles[0]
    placed = {first_tile: [0, 0, 0]}
    unplaced = tiles.copy()
    unplaced.remove(first_tile)
    while len(unplaced) != 0:
        found = set()
        for t in unplaced:
            rots = grids[t]
            for p in placed:
                placed_grid = grids[p][placed[p][2]]
                for i, rot in enumerate(rots):
                    found_rot = True
                    if check_top(rot, placed_grid):
                        placed[t] = [placed[p][0], placed[p][1] - 1, i]
                    elif check_right(rot, placed_grid):
                        placed[t] = [placed[p][0] - 1, placed[p][1], i]
                    elif check_bottom(rot, placed_grid):
                        placed[t] = [placed[p][0], placed[p][1] + 1, i]
                    elif check_left(rot, placed_grid):
                        placed[t] = [placed[p][0] + 1, placed[p][1], i]
                    else:
                        found_rot = False
                    if found_rot:
                        found.add(t)
                        break
                else:
                    continue
                break
        for f in found:
            unplaced.remove(f)
        if len(found) == 0:
            raise Exception("Error! Couldn't place all tiles.")
    return placed


def assemble_grid(grids, reconstructed_grid, outliers):
    min_x, max_x, min_y, max_y = outliers

    ret = []

    for i in range(max_y, min_y - 1, -1):
        row_grids = []
        for j in range(min_x, max_x + 1):
            grid = [grids[t][pos[2]] for t, pos in reconstructed_grid.items() if pos[0] == j and pos[1] == i][0]
            row_grids.append(grid)

        rows = [[] for i in range(len(row_grids[0]) - 2)]
        for grid in row_grids:
            for r in range(1, len(grid) - 1):
                rows[r - 1] += grid[r][1:-1]
        ret += rows
    return ret


SEA_MONSTER = """
                  # 
#    ##    ##    ###
 #  #  #  #  #  #   
"""


def parse_sea_monster():
    lines = [list(line) for line in SEA_MONSTER.split("\n")[1:-1]]
    return lines


def exists_sea_monster(grid, i, j, rot):
    for a in range(len(rot)):
        for b in range(len(rot[a])):
            if rot[a][b] == " ":
                continue
            try:
                if grid[i + a][j + b] != "#":
                    return False
            except IndexError:
                # grid doesn't fit
                return False
    return True


def remove_rough_seas(rough_seas, grid, i, j, rot):
    for a in range(len(rot)):
        for b in range(len(rot[a])):
            if rot[a][b] == " ":
                continue
            if grid[i + a][j + b] == "#":
                try:
                    rough_seas.remove([i + a, j + b])
                except ValueError:
                    pass


def find_sea_monsters(grid):
    rough_seas = [[i, j] for i in range(len(grid)) for j in range(len(grid[i])) if grid[i][j] == "#"]
    sea_monster = parse_sea_monster()
    rots = [sea_monster]
    rotated_grid = sea_monster
    for i in range(3):
        rotated_grid = rotate(rotated_grid)
        rots.append(rotated_grid)

    flipped_grid = flip(sea_monster)
    rots.append(flipped_grid)
    for i in range(3):
        flipped_grid = rotate(flipped_grid)
        rots.append(flipped_grid)

    for rot in rots:
        for i in range(len(grid)):
            for j in range(len(grid)):
                if exists_sea_monster(grid, i, j, rot):
                    remove_rough_seas(rough_seas, grid, i, j, rot)

    return rough_seas


def main():
    batches = read_batches("input.txt")

    grids = parse_batches(batches)

    reconstructed_grid = reconstruct(grids)

    grid_vals = reconstructed_grid.values()
    grid_x = [val[0] for val in grid_vals]
    grid_y = [val[1] for val in grid_vals]
    max_x = max(grid_x)
    min_x = min(grid_x)
    max_y = max(grid_y)
    min_y = min(grid_y)

    results = []
    for key, val in reconstructed_grid.items():
        if val[0] == min_x or val[0] == max_x:
            if val[1] == min_y or val[1] == max_y:
                results.append(key)

    assembled_grid = assemble_grid(grids, reconstructed_grid, [min_x, max_x, min_y, max_y])

    rough_waters = find_sea_monsters(assembled_grid)
    print(len(rough_waters))


if __name__ == "__main__":
    main()
