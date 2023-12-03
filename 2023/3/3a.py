from utils.input import read_file
from utils.grid import eight_around


def main():
    grid = read_file("input.txt")
    total = 0
    for y, row in enumerate(grid):
        current_int = ""
        symbol_found = False
        for x, col in enumerate(row):
            try:
                int(col)
                current_int += col
                surrounding = eight_around([y, x])
                for a, b in surrounding:
                    if a < 0 or b < 0:
                        continue
                    if a >= len(grid) or b >= len(row):
                        continue
                    if not grid[a][b] in "1234567890" and grid[a][b] != ".":
                        symbol_found = True
            except ValueError:
                if symbol_found:
                    total += int(current_int)
                current_int = ""
                symbol_found = False
        if symbol_found:
            total += int(current_int)
    print(total)


if __name__ == '__main__':
    main()