from utils.input import read_file


def read_rules(lines):
    rules = {}
    for line in lines:
        pair = line.split(" bags contain ")
        color = pair[0]
        print(color)
        contains = pair[1]
        if contains == "no other bags.":
            contain_counts = []
        else:
            contain_list = list(map(lambda x: x.strip(), contains.split(",")))
            contain_counts = [(int(x.split()[0]), " ".join(x.split()[1:-1])) for x in contain_list]
        print(contain_counts)
        rules[color] = contain_counts
    return rules


def part_1(lines):
    rules = read_rules(lines)
    seen = set()
    queue = ["shiny gold"]
    while queue:
        color = queue.pop()
        for source, dest in rules.items():
            for val in dest:
                if val[1] == color and source not in seen:
                    seen.add(source)
                    queue.append(source)
    print(seen)
    print(len(seen))


def part_2(lines):
    rules = read_rules(lines)
    counts = {}

    def count_bags(color):
        if color in counts:
            return counts[color]
        bag_counts = rules[color]
        totals = [bag[0] * count_bags(bag[1]) for bag in bag_counts]
        total = sum(totals)
        counts[color] = total + 1
        return counts[color]

    gold = count_bags("shiny gold")
    print(counts)
    print(gold)


def main():
    lines = read_file("7.txt")
    part_2(lines)


if __name__ == "__main__":
    main()
