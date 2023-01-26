from collections import defaultdict

import numpy as np

from utils.input import read_file, read_batches


def parse_input(batches):
    ret = []
    for batch in batches:
        scanner = []
        for beacon in batch[1:]:
            pts = [int(x) for x in beacon.split(",")]
            scanner.append(pts)
        ret.append(scanner)
    return ret


def compute_rotation_matrices():
    x = np.asarray([[1, 0, 0], [0, 0, -1], [0, 1, 0]])
    y = np.asarray([[0, 0, 1], [0, 1, 0], [-1, 0, 0]])
    z = np.asarray([[0, -1, 0], [1, 0, 0], [0, 0, 1]])

    ret = []
    curr = np.identity(3)
    for i in range(4):
        ret.append(curr)
        curr = z.dot(curr)
    curr = x.dot(curr)
    for i in range(4):
        for j in range(4):
            ret.append(curr)
            if i % 2 == 0:
                curr = y.dot(curr)
            else:
                curr = x.dot(curr)
        curr = z.dot(curr)
    curr = x.dot(curr)
    for i in range(4):
        ret.append(curr)
        curr = z.dot(curr)
    return ret


ROTATION_MATRICES = compute_rotation_matrices()


def compute_distance(pt1, pt2):
    """distance squared but w/e"""
    return (pt2[0] - pt1[0]) ** 2 + (pt2[1] - pt1[1]) ** 2 + (pt2[2] - pt1[2]) ** 2


def subtract(pt1, pt2):
    """Compute pt1 - pt2"""
    return [pt1[0] - pt2[0], pt1[1] - pt2[1], pt1[2] - pt2[2]]


def compute_distances(scanners):
    distances = []
    for scanner in scanners:
        scanner_dists = [[0 for i in range(len(scanner))] for j in range(len(scanner))]
        for i in range(len(scanner) - 1):
            for j in range(i + 1, len(scanner)):
                dist = compute_distance(scanner[i], scanner[j])
                scanner_dists[i][j] = dist
                scanner_dists[j][i] = dist
        distances.append(scanner_dists)
    return distances


def compare_scanner_distances(dists_1, dists_2):
    for i, pt_1 in enumerate(dists_1):
        for j, pt_2 in enumerate(dists_2):
            counts = defaultdict(int)
            for pt_a in pt_1:
                counts[pt_a] += 1
            for pt_b in pt_2:
                counts[pt_b] += 1
            filtered_counts = {k: v for k, v in counts.items() if v > 1 and k != 0}
            # Looking for 12 overlaps, which means 11 common distances from a point.
            if len(filtered_counts) < 11:
                continue
            filtered_keys = list(filtered_counts.keys())
            filtered_indices_1 = [i] + [pt_1.index(key) for key in filtered_keys]
            filtered_indices_2 = [j] + [pt_2.index(key) for key in filtered_keys]
            return True, filtered_indices_1, filtered_indices_2
    print("Not found...")
    return False, [], []


def compare_distances(scanner_distances):
    ret = []
    for i in range(len(scanner_distances) - 1):
        for j in range(i + 1, len(scanner_distances)):
            dists_1 = scanner_distances[i]
            dists_2 = scanner_distances[j]
            do_overlap, idx_1, idx_2 = compare_scanner_distances(dists_1, dists_2)
            if do_overlap:
                ret.append((i, j, idx_1, idx_2))
    return ret


def orient_points(pts, trans_idx):
    ret = []
    mat = ROTATION_MATRICES[trans_idx]
    for pt in pts:
        new_pt = mat.dot(pt)
        ret.append(list(new_pt))
    return ret


def orient_scanners(scanners, overlaps):
    """
    :param scanners: list of lists of 3D points
    :param overlaps: list of (scanner_1, scanner_2, indices_1, indices_2)
    :return:
    """
    rotations = {}
    for overlap in overlaps:
        s1 = scanners[overlap[0]]
        s2 = scanners[overlap[1]]
        pts_1 = [s1[i] for i in overlap[2]]
        pts_2 = [s2[i] for i in overlap[3]]

        target = subtract(pts_1[0], pts_1[1])
        current = subtract(pts_2[0], pts_2[1])
        print(f"{overlap[0]} {overlap[1]}")
        print(target)
        print(current)

        rotation_matrix = None
        inverse_rotation = None
        for i, rotation in enumerate(ROTATION_MATRICES):
            output = rotation.dot(current)
            if np.array_equal(output, target):
                rotation_matrix = i
            inverse = rotation.dot(target)
            if np.array_equal(inverse, current):
                inverse_rotation = i
            if rotation_matrix and inverse_rotation:
                break
        assert rotation_matrix is not None
        assert inverse_rotation is not None

        # How to get from overlap[1] to overlap[0].
        rotations[(overlap[0], overlap[1])] = rotation_matrix
        rotations[(overlap[1], overlap[0])] = inverse_rotation

    # Okay now we need to translate everything to scanner 0.
    # Say I have 0-1, 1-4, 1-3, 2-4.
    # I need 0-1, 0-2, 0-3, 0-4.
    # First, find all keys starting with 0.
    initial_keys = [k for k in rotations if k[0] == 0]
    q = []
    for k in initial_keys:
        second_key = k[1]
        second_keys = [k for k in rotations if k[0] == second_key]
        for k_2 in second_keys:
            q.append((k, k_2))
    while len(q) > 0:
        key_1, key_2 = q.pop(0)
        transitive_key = (key_1[0], key_2[1])
        if transitive_key in rotations:
            continue
        rot_idx_1 = rotations[key_1]
        rot_idx_2 = rotations[key_2]

        matrix_1 = ROTATION_MATRICES[rot_idx_1]
        matrix_2 = ROTATION_MATRICES[rot_idx_2]

        transitive_matrix = matrix_1.dot(matrix_2)
        inverse_matrix = transitive_matrix.T

        trans_idx = None
        inv_idx = None
        for i, mat in enumerate(ROTATION_MATRICES):
            if np.array_equal(transitive_matrix, mat):
                trans_idx = i
            if np.array_equal(inverse_matrix, mat):
                inv_idx = i
        assert trans_idx is not None
        assert inv_idx is not None

        rotations[transitive_key] = trans_idx
        rotations[(key_2[1], key_1[0])] = inv_idx

        second_keys = [k for k in rotations if k[0] == key_2[1]]
        for k_2 in second_keys:
            q.append((transitive_key, k_2))

    oriented_scanners = [scanners[0]]
    for i in range(1, len(scanners)):
        s = scanners[i]
        trans_idx = rotations[(0, i)]
        oriented_scanners.append(orient_points(s, trans_idx))
    return oriented_scanners


def plot_beacons(scanners, overlaps):
    beacons = set()
    relative_scanners = {}
    for overlap in overlaps:
        s1 = scanners[overlap[0]]
        s2 = scanners[overlap[1]]
        pts_1 = [s1[i] for i in overlap[2]]
        pts_2 = [s2[i] for i in overlap[3]]
        relative_scanners[(overlap[0], overlap[1])] = subtract(pts_1[0], pts_2[0])
        relative_scanners[(overlap[1], overlap[0])] = subtract(pts_2[0], pts_1[0])
    print(relative_scanners)

    initial_keys = [k for k in relative_scanners if k[0] == 0]
    q = []
    for k in initial_keys:
        second_key = k[1]
        second_keys = [k for k in relative_scanners if k[0] == second_key]
        for k_2 in second_keys:
            q.append((k, k_2))
    while len(q) > 0:
        key_1, key_2 = q.pop(0)
        transitive_key = (key_1[0], key_2[1])
        if transitive_key in relative_scanners:
            continue
        vec_1 = relative_scanners[key_1]
        vec_2 = relative_scanners[key_2]
        vec_sum = [vec_1[i] + vec_2[i] for i in range(3)]
        negative = [-a for a in vec_sum]
        relative_scanners[transitive_key] = vec_sum
        relative_scanners[(key_2[1], key_1[0])] = negative

        second_keys = [k for k in relative_scanners if k[0] == key_2[1]]
        for k_2 in second_keys:
            q.append((transitive_key, k_2))
    scanner_locs = [[0, 0, 0]]
    for i in range(1, len(scanners)):
        scanner_locs.append(relative_scanners[(0, i)])
    print(scanner_locs)

    for i, scanner in enumerate(scanners):
        scanner_loc = scanner_locs[i]
        for pts in scanner:
            beacon_loc = tuple(np.add(scanner_loc, pts))
            beacons.add(beacon_loc)
    return scanner_locs, beacons


def part_1():
    batches = read_batches("input.txt")
    scanners = parse_input(batches)
    distances = compute_distances(scanners)
    overlaps = compare_distances(distances)
    print(overlaps)

    oriented_scanners = orient_scanners(scanners, overlaps)
    scanner_locs, beacons = plot_beacons(oriented_scanners, overlaps)

    print(scanner_locs)
    print(beacons)
    print(len(beacons))

    highest = 0
    for i in range(len(scanner_locs) - 1):
        for j in range(i + 1, len(scanner_locs)):
            s1 = scanner_locs[i]
            s2 = scanner_locs[j]
            dist = subtract(s1, s2)
            manhattan = abs(dist[0]) + abs(dist[1]) + abs(dist[2])
            if manhattan > highest:
                highest = manhattan
    print(highest)


if __name__ == "__main__":
    part_1()
