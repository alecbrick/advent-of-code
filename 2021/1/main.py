from utils.input import read_file


def part_1():
    lines = read_file("1.txt")
    nums = [int(line) for line in lines]
    increases = 0
    for i in range(1, len(nums)):
        if nums[i] > nums[i - 1]:
            increases += 1
    print(increases)



def part_2():
    lines = read_file("1.txt")
    nums = [int(line) for line in lines]
    increases = 0
    for i in range(3, len(nums)):
        if nums[i] > nums[i - 3]:
            increases += 1
    print(increases)


if __name__ == "__main__":
    part_2()
