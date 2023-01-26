from collections import defaultdict

from utils.input import read_file, read_batches


def tokenize(line):
    tokens = []
    chars = line.split()
    paren_start = None
    paren_count = 0
    for i, c in enumerate(line):
        if c == " ":
            continue
        elif c == "(":
            if paren_count == 0:
                paren_start = i
            paren_count += 1
        elif c == ")":
            paren_count -= 1
            if paren_count == 0:
                paren_expr = line[paren_start + 1:i]
                tokens.append(tokenize(paren_expr))
        else:
            if paren_count == 0:
                if c.isdigit():
                    tokens.append(int(c))
                else:
                    tokens.append(c)
    return tokens


def evaluate_1(tokens):
    if isinstance(tokens, int):
        return tokens
    i = 2
    left = evaluate_1(tokens[0])
    while i < len(tokens):
        right = evaluate_1(tokens[i])
        operator = tokens[i - 1]
        if operator == "*":
            left = left * right
        elif operator == "+":
            left = left + right
        else:
            raise ValueError("What to heck!")
        i += 2
    return left


def evaluate_2(tokens):
    print(tokens)
    if isinstance(tokens, int):
        return tokens
    new_tokens = [evaluate_2(tokens[0])]
    i = 1
    while i < len(tokens):
        left = new_tokens[-1]
        right = evaluate_2(tokens[i + 1])
        operator = tokens[i]
        if operator == "*":
            new_tokens.append(operator)
            new_tokens.append(right)
        elif operator == "+":
            new_value = left + right
            new_tokens[-1] = new_value
        else:
            raise ValueError("What to heck!")
        i += 2

    left = new_tokens[0]
    i = 1
    while i < len(new_tokens):
        right = new_tokens[i + 1]
        left = left * right
        i += 2
    return left


def main():
    lines = read_file("input.txt")
    total = 0
    tokenized = []
    for line in lines:
        tokenized.append(tokenize(line))
    print(tokenized[0])

    answers = [evaluate_2(tokens) for tokens in tokenized]
    print(sum(answers))


if __name__ == "__main__":
    main()
