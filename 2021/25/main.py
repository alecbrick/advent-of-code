from utils.input import read_file


def parse_input(lines):
    ret = []
    for line in lines:
        ret.append(list(line))
    return ret


def step(board):
    new_board = [[board[i][j] for j in range(len(board[0]))] for i in range(len(board))]
    # Moving east
    for i in range(len(board)):
        for j in range(len(board[i])):
            sc = board[i][j]
            next_j = (j + 1) % (len(board[i]))
            next_sc = board[i][next_j]
            if sc == ">" and next_sc == ".":
                new_board[i][j] = "."
                new_board[i][next_j] = ">"
    board = new_board
    new_board = [[board[i][j] for j in range(len(board[0]))] for i in range(len(board))]
    # Moving south
    for i in range(len(board)):
        for j in range(len(board[i])):
            sc = board[i][j]
            next_i = (i + 1) % (len(board))
            next_sc = board[next_i][j]
            if sc == "v" and next_sc == ".":
                new_board[i][j] = "."
                new_board[next_i][j] = "v"
    return new_board


def part_1():
    lines = read_file("input.txt")
    board = parse_input(lines)
    print(board)
    moves = 0
    while True:
        new_board = step(board)
        moves += 1
        found = False
        for i in range(len(board)):
            if board[i] != new_board[i]:
                found = True
                break
        if not found:
            break
        board = new_board
    print(moves)


def part_2():
    lines = read_file("input.txt")


if __name__ == "__main__":
    part_1()
