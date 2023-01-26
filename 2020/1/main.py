from utils.input import read_file


def part_1():
    lines = read_file("1.txt")
    nums = [int(line) for line in lines]
    for i in range(0, len(nums) - 1):
        for j in range(i + 1, len(nums)):
            if nums[i] + nums[j] == 2020:
                print(nums[i] * nums[j])
                return


def part_2():
    lines = read_file("1.txt")
    nums = [int(line) for line in lines]
    for i in range(0, len(nums) - 2):
        for j in range(i + 1, len(nums) - 1):
            for k in range(j + 1, len(nums)):
                if nums[i] + nums[j] + nums[k] == 2020:
                    print(nums[i] * nums[j] * nums[k])
                    return


if __name__ == "__main__":
    part_2()
