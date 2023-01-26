import math
import heapq

from utils.input import read_file


def parse_input(_hex):
    ret = ""
    for h in _hex:
        bitz = int(h, 16)
        ret += format(bitz, "04b")
    return ret


def parse_type_4(bitz):
    """Returns the parsed number, and the `i` position after the last bit."""
    ret = ""
    for i in range(0, len(bitz), 5):
        sub_bitz = bitz[i:i + 5]
        ret += sub_bitz[1:]
        if sub_bitz[0] == "0":
            return int(ret, 2), i + 5


def parse_packet(bitz):
    version = int(bitz[:3], 2)
    type_id = int(bitz[3:6], 2)
    total_version = version
    if type_id == 4:
        num, i = parse_type_4(bitz[6:])
        return num, version, i + 6
    else:
        nums = []
        l_id = bitz[6]
        if l_id == "0":
            length_adder = 22
            length = int(bitz[7:22], 2)
            total_l = 0
            while total_l < length:
                num, v, l = parse_packet(bitz[22 + total_l:])
                total_version += v
                total_l += l
                nums.append(num)
        else:
            length_adder = 18
            length = int(bitz[7:18], 2)
            total_l = 0
            num_packets = 0
            while num_packets < length:
                num, v, l = parse_packet(bitz[18 + total_l:])
                total_version += v
                total_l += l
                num_packets += 1
                nums.append(num)
        if type_id == 0:
            ret_num = sum(nums)
        elif type_id == 1:
            ret_num = 1
            for n in nums:
                ret_num *= n
        elif type_id == 2:
            ret_num = min(nums)
        elif type_id == 3:
            ret_num = max(nums)
        elif type_id == 5:
            if nums[0] > nums[1]:
                ret_num = 1
            else:
                ret_num = 0
        elif type_id == 6:
            if nums[0] < nums[1]:
                ret_num = 1
            else:
                ret_num = 0
        elif type_id == 7:
            if nums[0] == nums[1]:
                ret_num = 1
            else:
                ret_num = 0
        else:
            raise ValueError(type_id)
        return ret_num, total_version, total_l + length_adder


def part_1():
    _hex = read_file("input.txt")[0]
    bitz = parse_input(_hex)
    num, v, l = parse_packet(bitz)
    print(num)
    print(v)
    print(l)


def part_2():
    lines = read_file("input.txt")


if __name__ == "__main__":
    part_1()
