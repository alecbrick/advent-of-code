from utils.input import read_file


def main():
    lines = read_file("input.txt")
    total = 0
    for i, line in enumerate(lines):
        highest = {
            "red": 0,
            "green": 0,
            "blue": 0,
        }
        line = line.split(":")[1].strip()
        draws = line.split("; ")
        for draw in draws:
            counts = draw.split(", ")
            for count in counts:
                amount, color = count.split(" ")
                if int(amount) > highest[color]:
                    highest[color] = int(amount)
        total += (highest["red"] * highest["green"] * highest["blue"])
    print(total)


if __name__ == '__main__':
    main()