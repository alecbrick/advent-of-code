

def read_file(filename, strip=True):
    with open(filename) as file:
        lines = [line for line in file.readlines()]
        if strip:
            lines = [line.strip() for line in lines]
        else:
            lines = [line[:-1] for line in lines]
        return lines


def read_batches(filename, strip=True):
    lines = read_file(filename, strip)
    batches = []
    batch = []
    for line in lines:
        if line == "":
            batches.append(batch)
            batch = []
        else:
            batch.append(line)

    batches.append(batch)
    return batches
