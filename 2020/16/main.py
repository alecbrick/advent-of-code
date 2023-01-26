from utils.input import read_file, read_batches
from utils.narrow_down import narrow_down

rules = {
    "dl":  [[32, 615], [626, 955]],
    "ds": [[47, 439], [454, 961]],
    "dp": [[31, 98], [119, 969]],
    "dt": [[45, 746], [763, 967]],
    "dd": [[49, 723], [736, 954]],
    "dti": [[42, 556], [581, 962]],
    "al": [[46, 401], [418, 964]],
    "as": [[39, 281], [295, 974]],
    "ap": [[43, 80], [99, 950]],
    "at": [[28, 670], [682, 959]],
    "class": [[43, 504], [520, 957]],
    "duration": [[31, 358], [365, 959]],
    "price": [[41, 626], [650, 956]],
    "route": [[26, 488], [495, 949]],
    "row": [[46, 913], [931, 965]],
    "seat": [[40, 223], [249, 958]],
    "train": [[32, 832], [853, 966]],
    "type": [[36, 776], [798, 960]],
    "wagon": [[38, 122], [134, 969]],
    "zone": [[27, 870], [885, 952]],
}


def validate_num(num):
    for name, ranges in rules.items():
        range_0 = range(ranges[0][0], ranges[0][1] + 1)
        range_1 = range(ranges[1][0], ranges[1][1] + 1)
        if num in range_0 or num in range_1:
            return True
    return False


def validate_with_rule(num, rule_name):
    r = rules[rule_name]
    range_0 = range(r[0][0], r[0][1] + 1)
    range_1 = range(r[1][0], r[1][1] + 1)
    if num in range_0 or num in range_1:
        return True
    return False


def validate_tickets(lines):
    total = 0
    ret = []
    for line in lines:
        vals = [int(l) for l in line.split(",")]
        for val in vals:
            if not validate_num(val):
                break
        else:
            ret.append(vals)
    return ret


def find_fields(lines):
    possibilities = {
        name: [i for i in range(len(rules))]
        for name in rules.keys()
    }

    for line in lines:
        for i, val in enumerate(line):
            for name in rules.keys():
                if not validate_with_rule(val, name):
                    try:
                        possibilities[name].remove(i)
                    except Exception:
                        pass
    return possibilities


def main():
    lines = read_file("input.txt")
    my_ticket = [191,61,149,157,79,197,67,139,59,71,163,53,73,137,167,173,193,151,181,179]

    good_tickets = validate_tickets(lines)
    print(good_tickets)
    possibilities = find_fields(good_tickets)
    print(possibilities)
    narrowed = narrow_down(possibilities)
    print(narrowed)

    print(f"Solution: {my_ticket[12] * my_ticket[8] * my_ticket[4] * my_ticket[14] * my_ticket[19] * my_ticket[2]}")


if __name__ == "__main__":
    main()
