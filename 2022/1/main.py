from utils.input import read_file, read_batches


def part_1():
    batches = read_batches("1.txt")
    num_batches = [[int(line) for line in batch] for batch in batches]
    highest = 0
    for batch in num_batches:
        count = sum(batch)
        if count > highest:
            highest = count
    print(highest)


def part_2():
    batches = read_batches("1.txt")
    num_batches = [[int(line) for line in batch] for batch in batches]
    sum_batches = [sum(batch) for batch in num_batches]
    sorted_batches = sorted(sum_batches, reverse=True)
    print(sum(sorted_batches[:3]))


if __name__ == "__main__":
    part_2()
