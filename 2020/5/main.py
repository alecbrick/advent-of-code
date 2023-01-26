from utils.input import read_file


NUM_ROWS = 128
NUM_COLS = 8


def binary_search(spec, size):
    curr_min = 0
    curr_max = size
    for char in spec[:-1]:
        center = (curr_min + curr_max) / 2
        if char == "F" or char == "L":
            curr_max = center
        else:
            curr_min = center
    last = spec[-1]
    if last == "F" or last == "L":
        return curr_min
    else:
        return curr_min + 1


def get_seat(line):
    row_spec = line[:7]
    col_spec = line[7:]
    row = binary_search(row_spec, NUM_ROWS)
    col = binary_search(col_spec, NUM_COLS)
    return row, col


def main():
    lines = read_file("5.txt")
    seats = [get_seat(line) for line in lines]
    seat_ids = [8 * seat[0] + seat[1] for seat in seats]
    for i in range(0, 128 * 8):
        if i not in seat_ids:
            print(i)
    print(max(seat_ids))


if __name__ == "__main__":
    main()
