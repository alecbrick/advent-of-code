from utils.input import read_file


def say_numbers(input, stop=2020):
    i = 0
    previous_mentions = {}
    last_mentions = {}
    for num in input:
        if num in last_mentions:
            previous_mentions[num] = last_mentions[i]
        last_mentions[num] = i
        i += 1

    last_said = input[-1]
    while i < stop:
        if last_said not in previous_mentions:
            num = 0
        else:
            num = last_mentions[last_said] - previous_mentions[last_said]
        if num in last_mentions:
            previous_mentions[num] = last_mentions[num]
        last_mentions[num] = i
        last_said = num
        i += 1
    return last_said


def main():
    input = [11, 0, 1, 10, 5, 19]
    sol = say_numbers(input, 30000000)
    print(f"Solution: {sol}")


if __name__ == "__main__":
    main()
