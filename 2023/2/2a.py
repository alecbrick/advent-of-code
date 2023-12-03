from utils.input import read_file


def main():
    lines = read_file("input.txt")
    total = 0
    limits = {
        "red": 12,
        "green": 13,
        "blue": 14,
    }
    for i, line in enumerate(lines):
        line = line.split(":")[1].strip()
        draws = line.split("; ")
        possible = True
        for draw in draws:
            counts = draw.split(", ")
            for count in counts:
                amount, color = count.split(" ")
                if int(amount) > limits[color]:
                    possible = False
        if possible:
            total += i + 1
    print(total)


if __name__ == '__main__':
    main()