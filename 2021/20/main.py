from utils.input import read_batches


def parse_input(batches):
    ret = []
    for line in batches[1]:
        ret.append(list(line))
    return batches[0][0], ret


def iterate(alg, img, infinite_space):
    output = [[None for i in range(len(img) + 2)] for j in range(len(img) + 2)]
    expanded_img = [[infinite_space for i in range(len(img) + 4)] for j in range(len(img) + 4)]
    for i in range(len(img)):
        for j in range(len(img[i])):
            expanded_img[i + 2][j + 2] = img[i][j]
    for i in range(len(output)):
        for j in range(len(output[i])):
            a, b = i + 1, j + 1
            num = expanded_img[a - 1][b - 1:b+2] + expanded_img[a][b - 1:b + 2] + expanded_img[a + 1][b - 1:b + 2]
            num = ''.join(['0' if s == '.' else '1' for s in num])
            num = int(num, 2)
            c = alg[num]
            output[i][j] = c
    return output, "#" if infinite_space == "." else "."


def part_1():
    batches = read_batches("input.txt")
    alg, img = parse_input(batches)
    inf_space = "."
    for i in range(50):
        new_img, inf_space = iterate(alg, img, inf_space)
        img = new_img
    total = 0
    for row in img:
        for c in row:
            if c == "#":
                total += 1
    for row in img:
        print(''.join(row))
    print(total)


def part_2():
    batches = read_batches("input.txt")


if __name__ == "__main__":
    part_1()
