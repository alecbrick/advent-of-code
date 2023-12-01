from utils.input import read_file

possible = [
    "0", "1", "2", "3", "4", "5", "6", "7", "8", "9",
    "zero", "one", "two", "three", "four", "five",
    "six", "seven", "eight", "nine"
]

mapping = {a: b for (a, b) in zip(possible[10:], possible[:10])}

def main():
    lines = read_file('1a.txt')

    total = 0
    for line in lines:
        earliest = (None, None)
        latest = (None, None)
        for c in possible:
            for i in range(len(line)):
                if line[i:].startswith(c):
                    if earliest[0] is None or i < earliest[0]:
                        earliest = (i, c)
                    if latest[0] is None or i > latest[0]:
                        latest = (i, c)

        total += int(mapping.get(earliest[1], earliest[1]) + mapping.get(latest[1], latest[1]))
        print(earliest, latest)
    print(total)


if __name__ == '__main__':
    main()