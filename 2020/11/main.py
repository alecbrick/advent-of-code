from utils.input import read_file


def is_out_of_bounds(i, j, rows, cols):
    if i < 0 or i >= rows:
        return True
    if j < 0 or j >= cols:
        return True
    return False


def iterate(lines, tolerance=4):
    new_lines = []
    for i, line in enumerate(lines):
        new_line = []
        for j, char in enumerate(line):
            if char == ".":
                new_line.append(".")
                continue
            neighbors = 0
            for a in [-1, 0, 1]:
                for b in [-1, 0, 1]:
                    if a == 0 and b == 0:
                        continue
                    c = i + a
                    d = j + b
                    while not is_out_of_bounds(c, d, len(lines), len(line)):
                        if lines[c][d] == "L":
                            break
                        if lines[c][d] == "#":
                            neighbors += 1
                            break
                        c += a
                        d += b
            if char == "L" and neighbors == 0:
                new_line.append("#")
            elif char == "#" and neighbors >= tolerance:
                new_line.append("L")
            else:
                new_line.append(char)
        new_lines.append(new_line)
    return new_lines


def count_occupied(lines):
    total = 0
    for line in lines:
        for char in line:
            if char == "#":
                total += 1
    return total


def pretty_print(lines):
    for line in lines:
        print("".join(line))
    print("")


def only_part(lines):
    count = 0
    while True:
        new_lines = iterate(lines, 5)
        pretty_print(new_lines)
        if new_lines == lines:
            total = count_occupied(lines)
            print(f"Iterations: {count}")
            print(f"Solution: {total}")
            break
        lines = new_lines
        count += 1


def main():
    lines = read_file("11.txt")
    only_part(lines)


if __name__ == "__main__":
    main()
