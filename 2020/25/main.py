from utils.input import read_file


def exp_mod(val, sub, mod=20201227):
    new_val = val * sub
    return new_val % mod


def transform(subj, loop, mod=20201227):
    val = (subj ** loop) % mod
    return val


def find_loop(val, subj=7):
    loop = 1
    curr = subj
    while curr != val:
        curr = exp_mod(curr, subj)
        loop += 1
    return loop


def main():
    card_pub_key = 3469259
    door_pub_key = 13170438

    card_loop = find_loop(card_pub_key)
    key = transform(door_pub_key, card_loop)
    print(key)


if __name__ == "__main__":
    main()
