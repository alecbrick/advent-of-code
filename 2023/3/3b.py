from collections import defaultdict

from utils.input import read_file
from utils.grid import eight_around


def main():
    grid = read_file("input.txt")
    total = 0
    stars = defaultdict(list)
    for y, row in enumerate(grid):
        current_int = ""
        current_stars = set()
        for x, col in enumerate(row):
            if col in "1234567890":
                current_int += col
                surrounding = eight_around([y, x])
                for a, b in surrounding:
                    if a < 0 or b < 0:
                        continue
                    if a >= len(grid) or b >= len(row):
                        continue
                    if grid[a][b] == "*":
                        current_stars.add((a, b))
            else:
                for star in current_stars:
                    stars[star].append(int(current_int))
                current_int = ""
                current_stars = set()
        for star in current_stars:
            stars[star].append(int(current_int))
    for star, nums in stars.items():
        print(star, nums)
        if len(nums) == 2:
            total += nums[0] * nums[1]
    print(total)


if __name__ == '__main__':
    main()