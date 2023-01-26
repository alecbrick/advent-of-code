from collections import defaultdict

from utils.input import read_file



def is_incomplete(line):
    l_total = 0
    r_total = 0
    for c in line:
        if c in "([{<":
            l_total += 1
        else:
            r_total += 1
    return l_total > r_total


pairs = {
    ")": "(",
    "]": "[",
    "}": "{",
    ">": "<"
}

reverse_pairs = {
    v: k for k, v in pairs.items()
}

scores = {
    ")": 3,
    "]": 57,
    "}": 1197,
    ">": 25137
}

def part_1():
    lines = read_file("input.txt")
    total = 0
    for line in lines:
        """
        if is_incomplete(line):
            continue
        """
        stack = []
        for c in line:
            if c in "([{<":
                stack.append(c)
            else:
                if len(stack) == 0:
                    # Incomplete
                    print("Incomplete, skpiping")
                    break
                top = stack.pop()
                if pairs[c] != top:
                    total += scores[c]
                    break
    print(total)




def dfs(rows, i, j, visited):
    if (i, j) in visited:
        return []
    if i < 0 or j < 0 or i >= len(rows) or j >= len(rows[0]):
        return []
    if rows[i][j] == 9:
        return []
    visited.append((i, j))
    up = dfs(rows, i - 1, j, visited)
    down = dfs(rows, i + 1, j, visited)
    left = dfs(rows, i, j - 1, visited)
    right = dfs(rows, i, j + 1, visited)
    return [(i, j)] + up + down + left + right


scores_2 = {
    "(": 1,
    "[": 2,
    "{": 3,
    "<": 4
}


def part_2():
    lines = read_file("input.txt")
    all_scores = []
    for line in lines:
        stack = []
        corrupted = False
        for c in line:
            if c in "([{<":
                stack.append(c)
            else:
                top = stack.pop()
                if pairs[c] != top:
                    corrupted = True
                    break
        if corrupted:
            continue
        total = 0
        while len(stack) > 0:
            c = stack.pop()
            total *= 5
            total += scores_2[c]
        all_scores.append(total)
    sorted_scores = sorted(all_scores)
    middle_score = sorted_scores[(len(sorted_scores) - 1) // 2]
    print(middle_score)


if __name__ == "__main__":
    part_2()
