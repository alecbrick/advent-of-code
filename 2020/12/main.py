from utils.input import read_file


def navigate_1(directions):
    x = 0
    y = 0
    deg = 0
    for dir, num in directions:
        if dir == "N":
            y += num
        elif dir == "E":
            x += num
        elif dir == "S":
            y -= num
        elif dir == "W":
            x -= num
        elif dir == "R":
            deg = (deg - num) % 360
        elif dir == "L":
            deg = (deg + num) % 360
        elif dir == "F":
            if deg == 0:
                x += num
            elif deg == 90:
                y += num
            elif deg == 180:
                x -= num
            elif deg == 270:
                y -= num
            else:
                raise ValueError(f"Unexpected degrees: {deg}")
    return x, y


def navigate_2(directions):
    x = 0
    y = 0
    way_x = 10
    way_y = 1
    for dir, num in directions:
        if dir == "N":
            way_y += num
        elif dir == "E":
            way_x += num
        elif dir == "S":
            way_y -= num
        elif dir == "W":
            way_x -= num
        elif dir == "R":
            while num > 0:
                temp = way_y
                way_y = -way_x
                way_x = temp
                num -= 90
        elif dir == "L":
            while num > 0:
                temp = way_x
                way_x = -way_y
                way_y = temp
                num -= 90
        elif dir == "F":
            x += num * way_x
            y += num * way_y
    return x, y


def parse_directions(lines):
    return [(line[0], int(line[1:])) for line in lines]


def run(lines):
    directions = parse_directions(lines)
    new_x, new_y = navigate_2(directions)
    print(f"Solution: {abs(new_x) + abs(new_y)}")


def main():
    lines = read_file("12.txt")
    run(lines)


if __name__ == "__main__":
    main()
