def eight_around(coords):
    ret = []
    y, x = coords
    for a in [-1, 0, 1]:
        for b in [-1, 0, 1]:
            if a == 0 and b == 0:
                continue
            ret.append((y + a, x + b))
    return ret
