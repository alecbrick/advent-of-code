from utils.input import read_file


def main():
    lines = read_file('1a.txt')
    total = 0
    for line in lines:
        first_seen = None
        last_seen = None
        for c in line:
            try:
                int(c)
                if first_seen is None:
                    first_seen = c
                last_seen = c
            except ValueError:
                pass
        total += int(first_seen + last_seen)
    print(total)


if __name__ == '__main__':
    main()