def narrow_down(possibilities):
    confirmed = set()
    end = False
    while not end:
        end = True
        for name, lst in possibilities.items():
            if len(lst) == 1:
                if lst[0] in confirmed:
                    continue
                end = False
                confirmed.add(lst[0])
                for n in possibilities.keys():
                    if name == n:
                        continue
                    try:
                        possibilities[n].remove(lst[0])
                    except Exception:
                        continue
    return possibilities


def narrow_down_sets(possibilities):
    possibilities = {
        k: list(v) for k, v in possibilities.items()
    }
    return narrow_down(possibilities)
