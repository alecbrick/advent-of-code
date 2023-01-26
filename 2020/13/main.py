from utils.input import read_file


def part_1(timestamp, bus_ids):
    mins = (0, None)
    for i in bus_ids:
        next_time = ((timestamp // i) + 1) * i
        diff = next_time - timestamp
        if not mins[1] or diff < mins[1]:
            mins = (i, diff)
    print(f"Found: {mins[0] * mins[1]}")


def sieve(a_n_pairs):
    a_n_pairs = sorted(a_n_pairs, key=lambda x: x[0], reverse=True)
    curr_a, curr_n = a_n_pairs[0]
    curr_val = curr_a
    for i in range(len(a_n_pairs) - 1):
        seeking_a, seeking_n = a_n_pairs[i + 1]
        while True:
            if curr_val % seeking_n == seeking_a:
                break
            curr_val += curr_n
        curr_n *= seeking_n
    return curr_val


def part_2(bus_ids):
    """
    7, 14, 21, 28, 35, 42, ..., 1068781 (x = 0 mod 7)
    12, 25, 38, 51, 64, ..., 1068781 (x = 12 mod 13)
    12, 31, 50, 69    (x = 12 mod 19)
    y = 7x
    y = 13x - 1
    y = 19x - 7

    t = m_1 * x_2 - b_2
    """

    a_n_pairs = []
    for i, _id in enumerate(bus_ids):
        if _id == "x":
            continue
        int_id = int(_id)
        a_n_pairs.append(((int_id - i) % int_id, int_id))
    sol = sieve(a_n_pairs)
    print(f"Found! {sol}")


def main():
    lines = read_file("13.txt")
    timestamp = int(lines[0])
    bus_ids = [i for i in lines[1].split(",")]
    part_2(bus_ids)


if __name__ == "__main__":
    main()
