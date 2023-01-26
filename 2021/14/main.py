from collections import defaultdict

from utils.input import read_file, read_batches


def parse_expansions(lines):
    ret = {}
    for line in lines:
        pair = line.split(" -> ")
        ret[pair[0]] = pair[1]
    return ret


def part_1():
    batches = read_batches("input.txt")

    template = batches[0][0]
    expansions = parse_expansions(batches[1])
    print(template)
    print(expansions)
    counts = defaultdict(int)
    for i in range(len(template) - 1):
        pair = template[i:i + 2]
        counts[pair] += 1
    iterations = 40
    for i in range(iterations):
        new_counts = defaultdict(int)
        for pair, count in counts.items():
            output = expansions[pair]
            pair_1 = pair[0] + output
            pair_2 = output + pair[1]
            new_counts[pair_1] += count
            new_counts[pair_2] += count
        counts = new_counts
        print(counts)
    print(counts)

    letter_counts = defaultdict(int)
    for pair, count in counts.items():
        for letter in pair:
            letter_counts[letter] += count
    print(letter_counts)
    letter_counts[template[0]] += 1
    letter_counts[template[-1]] += 1
    for letter in letter_counts:
        letter_counts[letter] //= 2
    print(letter_counts)
    kv = [(k, v) for k, v in letter_counts.items()]
    kv_sorted = sorted(kv, key=lambda x: x[1])
    print(kv_sorted[-1][1] - kv_sorted[0][1])


if __name__ == "__main__":
    part_1()
