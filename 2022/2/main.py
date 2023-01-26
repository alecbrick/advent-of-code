from utils.input import read_file, read_batches

abc = ["A", "B", "C"]
xyz = ["X", "Y", "Z"]


def score_round(them, us):
    them_index = abc.index(them)
    us_index = xyz.index(us)
    us_score = us_index + 1
    if us_index == them_index:
        points = 3
    elif (us_index + 1) % 3 == them_index:
        points = 0
    else:
        points = 6
    return us_score + points


def score_round_2(them, us):
    them_index = abc.index(them)
    us_index = xyz.index(us)
    points = us_index * 3
    if us == "X":
        new_ind = (them_index - 1) % 3
    elif us == "Y":
        new_ind = them_index
    else:
        new_ind = (them_index + 1) % 3
    return points + new_ind + 1


def part_1():
    lines = read_file("input.txt")
    total = 0
    for line in lines:
        them, us = line.split()
        score = score_round(them, us)
        print(score)
        total += score
    print(total)


def part_2():
    lines = read_file("input.txt")
    total = 0
    for line in lines:
        them, us = line.split()
        score = score_round_2(them, us)
        print(score)
        total += score
    print(total)


if __name__ == "__main__":
    part_2()
