from utils.input import read_file


def parse_line(line):
    command = line.split()
    return command[0], int(command[1])


def parse_input(lines):
    numbers = lines[0]
    numbers = [int(n) for n in numbers.split(",")]
    boards = []
    for i in range(2, len(lines), 6):
        board = lines[i:i + 5]
        n_board = []
        for row in board:
            n_row = [int(n) for n in row.split()]
            n_board.append(n_row)
        boards.append(n_board)
    return numbers, boards


def has_won(status):
    for row in status:
        found_false = False
        for r in row:
            if not r:
                found_false = True
                break
        if not found_false:
            return True
    for i in range(5):
        has_false = False
        for j in range(5):
            if not status[j][i]:
                has_false = True
                break
        if not has_false:
            return True
    return False


def final_score(board, status, last_num):
    s = 0
    for i in range(5):
        for j in range(5):
            if not status[i][j]:
                s += board[i][j]
    print(board)
    print(status)
    print(last_num)
    print(s)
    return s * last_num


def part_1():
    lines = read_file("input.txt")
    numbers, boards = parse_input(lines)

    status = [
        [
            [False for _ in range(5)] for _ in range(5)
        ] for _ in range(len(boards))
    ]
    for num in numbers:
        for x, b in enumerate(boards):
            for i, row in enumerate(b):
                for j, n in enumerate(row):
                    if n == num:
                        status[x][i][j] = True
            if has_won(status[x]):
                print("I won!")
                print(status[x])
                print(final_score(b, status[x], num))
                return


def part_2():
    lines = read_file("input.txt")
    numbers, boards = parse_input(lines)

    status = [
        [
            [False for _ in range(5)] for _ in range(5)
        ] for _ in range(len(boards))
    ]
    won = [(False, 0) for _ in range(len(boards))]
    last_won = 0
    for num in numbers:
        for x, b in enumerate(boards):
            if won[x][0]:
                continue
            for i, row in enumerate(b):
                for j, n in enumerate(row):
                    if n == num:
                        status[x][i][j] = True
            if has_won(status[x]):
                last_won = x
                won[x] = (True, num)
    print("I won!")
    print(status[last_won])
    print(final_score(boards[last_won], status[last_won], won[last_won][1]))
    return



if __name__ == "__main__":
    part_2()
