from utils.input import read_file


FIELDS = [
    "ecl",
    "pid",
    "eyr",
    "hcl",
    "byr",
    "iyr",
    "cid",
    "hgt"
]

EYE_COLORS = ["amb", "blu", "brn", "gry", "grn", "hzl", "oth"]


def validate_hair(hcl):
    if len(hcl) != 7:
        return False
    if hcl[0] != "#":
        return False
    try:
        int(hcl[1:], 16)
        return True
    except ValueError:
        return False


def validate_height(hgt):
    if len(hgt) < 2:
        return False
    units = hgt[-2:]
    if not (units == "in" or units == "cm"):
        return False
    val = hgt[:-2]
    if len(val) < 2:
        return False
    if not val.isdigit():
        return False
    if units == "in":
        return 59 <= int(val) <= 76
    if units == "cm":
        return 150 <= int(val) <= 193
    raise ValueError("What to heck!")


VALIDATIONS = {
    "ecl": (lambda x: x in EYE_COLORS),
    "pid": (lambda x: x.isdigit() and len(x) == 9),
    "eyr": (lambda x: x.isdigit() and 2020 <= int(x) <= 2030),
    "hcl": validate_hair,
    "byr": (lambda x: x.isdigit() and 1920 <= int(x) <= 2002),
    "iyr": (lambda x: x.isdigit() and 2010 <= int(x) <= 2020),
    "cid": (lambda x: True),
    "hgt": validate_height,
}


def part_1(batches):
    good = 0
    for batch in batches:
        fields = batch.split(" ")
        pairs = [field.split(":") for field in fields]
        seen_fields = [pair[0] for pair in pairs]
        missing_fields = [field for field in FIELDS if field not in seen_fields]
        if missing_fields == [] or missing_fields == ["cid"]:
            print(f"Good: {batch}")
            good += 1
        else:
            print(f"Bad: {batch}")
    print(good)


def part_2(batches):
    good = 0
    for batch in batches:
        fields = batch.split(" ")
        pairs = [field.split(":") for field in fields]
        seen_fields = [pair[0] for pair in pairs]
        missing_fields = [field for field in FIELDS if field not in seen_fields]
        if not (missing_fields == [] or missing_fields == ["cid"]):
            print(f"Missing fields: {batch}")
            continue
        validations = [VALIDATIONS[pair[0]](pair[1]) for pair in pairs]
        failed = [v for v in validations if not v]
        if len(failed) > 0:
            print(f"Bad validation: {batch}")
            continue
        print(f"Good! {batch}")
        good += 1
    print(good)


def main():
    lines = read_file("4.txt")
    batches = []
    batch = []
    for line in lines:
        if line == "":
            full_batch = " ".join(batch)
            batches.append(full_batch)
            batch = []
        else:
            batch.append(line)

    full_batch = " ".join(batch)
    batches.append(full_batch)

    part_2(batches)


if __name__ == "__main__":
    main()

