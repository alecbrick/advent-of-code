import itertools
from collections import defaultdict

from utils.input import read_file, read_batches


def parse_rules(lines):
    base_rules = {}
    recursive_rules = {}
    for line in lines:
        pair = line.split(": ")
        rule_num = int(pair[0])
        if "\"" in pair[1]:
            base_rules[rule_num] = pair[1][1]
            continue
        options = pair[1].split(" | ")
        options = [list(map(int, o.split())) for o in options]
        recursive_rules[rule_num] = options
    return {
        "base": base_rules,
        "recursive": recursive_rules
    }


def find_possible_words(rule_num, rules, possible_words):
    if rule_num in possible_words:
        return possible_words[rule_num]
    if rule_num in rules["base"]:
        possible_words[rule_num] = [rules["base"][rule_num]]
        return possible_words[rule_num]
    rule = rules["recursive"][rule_num]
    ret = []
    for option in rule:
        poss = find_possible_words(option[0], rules, possible_words)
        if len(option) > 1:
            poss_1 = find_possible_words(option[1], rules, possible_words)
            poss = [pair[0] + pair[1] for pair in itertools.product(poss, poss_1)]
        ret += poss
    possible_words[rule_num] = ret
    return ret


def satisfies(string, rule, rules, possible_words):
    if len(string) == 0:
        return False
    if rule in possible_words:
        return string in possible_words[rule]
    if rule == 8:
        if string in possible_words[42]:
            return True
        for i in range(len(string)):
            prefix = string[:i + 1]
            suffix = string[i + 1:]
            if prefix in possible_words[42]:
                if satisfies(suffix, 8, rules, possible_words):
                    return True
        return False
    elif rule == 11:
        for i in range(len(string) - 1):
            for j in range(1, len(string)):
                prefix = string[:i + 1]
                center = string[i + 1:j]
                suffix = string[j:]
                if prefix in possible_words[42]:
                    if suffix in possible_words[31]:
                        if center == "" or satisfies(center, 11, rules, possible_words):
                            return True
        return False
    elif rule == 0:
        for i in range(len(string)):
            prefix = string[:i + 1]
            suffix = string[i + 1:]
            if satisfies(prefix, 8, rules, possible_words):
                if satisfies(suffix, 11, rules, possible_words):
                    return True
        return False
    else:
        raise ValueError("What to heck??")


def main():
    batches = read_batches("input.txt")
    rules = parse_rules(batches[0])
    lines = batches[1]

    possible_words = {}
    for rule in [42, 31]:
        find_possible_words(rule, rules, possible_words)

    sol = [line for line in lines if satisfies(line, 0, rules, possible_words)]
    print(f"Solution: {len(sol)}")


if __name__ == "__main__":
    main()
