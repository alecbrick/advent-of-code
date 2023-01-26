from utils.input import read_file, read_batches


def part_1(batches):
    print(batches)
    totals = []
    for batch in batches:
        seen = None
        for line in batch:
            seen = seen.intersection(set(line)) if seen is not None else set(line)
        totals.append(len(seen))
    print(totals)
    print(sum(totals))


def main():
    batches = read_batches("6.txt")
    part_1(batches)


if __name__ == "__main__":
    main()
