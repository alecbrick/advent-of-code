from collections import defaultdict


def part_1():
    pos = [6, 1]

    scores = [0, 0]
    turn = 0
    state = 0
    die_rolls = 0
    while True:
        steps = ((state + 1) + (state + 2) + (state + 3)) % 100
        pos[turn] = (pos[turn] + steps) % 10
        scores[turn] += pos[turn] + 1
        die_rolls += 3
        if scores[turn] >= 1000:
            break

        state += 3
        state = state % 100
        turn = (turn + 1) % 2
    print(die_rolls * scores[turn - 1])


def compute_possiblities():
    return [(i, j, k) for i in range(1, 4) for j in range(1, 4) for k in range(1, 4)]


possibilities = [sum(p) for p in compute_possiblities()]


def part_2():

    state_to_count = defaultdict(int)
    # Position, position, score, score
    state_to_count[(6, 1, 0, 0)] = 1
    turn = 0
    wins = [0, 0]
    while True:
        new_state_to_count = defaultdict(int)
        for state, count in state_to_count.items():
            pos = [state[0], state[1]]
            scores = [state[2], state[3]]

            for i in possibilities:
                new_pos = [pos[0], pos[1]]
                new_score = [scores[0], scores[1]]
                new_pos[turn] = (pos[turn] + i) % 10
                new_score[turn] += new_pos[turn] + 1
                if new_score[turn] >= 21:
                    wins[turn] += count
                else:
                    new_state_to_count[(new_pos[0], new_pos[1], new_score[0], new_score[1])] += count
        state_to_count = new_state_to_count
        turn = (turn + 1) % 2
        if len(state_to_count) == 0:
            break

    print(wins)


if __name__ == "__main__":
    part_2()
