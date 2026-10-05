import random

jigsaw_size = 9
max_steps = 1500
steps = 0


def get_neighbors(r, c):
    for dr, dc in ((-1, 0), (1, 0), (0, -1), (0, 1)):
        nr, nc = r + dr, c + dc
        if 0 <= nr < 9 and 0 <= nc < 9:
            yield nr, nc


def dead_region(matrix, sizes):
    for k in range(9):
        if 0 < sizes[k] < jigsaw_size:
            has_room = False
            for r in range(9):
                for c in range(9):
                    if matrix[r][c] == k:
                        if any(matrix[nr][nc] == -1 for nr, nc in get_neighbors(r, c)):
                            has_room = True
                            break
                if has_room:
                    break
            if not has_room:
                return True

    for r in range(9):
        for c in range(9):
            if matrix[r][c] == -1:
                if all(matrix[nr][nc] != -1 and sizes[matrix[nr][nc]] == jigsaw_size
                       for nr, nc in get_neighbors(r, c)):
                    return True
    return False


def fill(matrix, sizes):
    global steps
    steps += 1
    if steps > max_steps:
        return False

    k = None
    for i in range(9):
        if sizes[i] < jigsaw_size and (k is None or sizes[i] < sizes[k]):
            k = i

    if k is None:
        return True

    options = set()
    for r in range(9):
        for c in range(9):
            if matrix[r][c] == k:
                for nr, nc in get_neighbors(r, c):
                    if matrix[nr][nc] == -1:
                        options.add((nr, nc))

    options = list(options)
    random.shuffle(options)

    for r, c in options:
        matrix[r][c] = k
        sizes[k] += 1
        if not dead_region(matrix, sizes):
            if fill(matrix, sizes):
                return True
        matrix[r][c] = -1
        sizes[k] -= 1

    return False


def generate_regions():
    global steps
    while True:
        matrix = [[-1] * 9 for _ in range(9)]
        sizes = [0] * 9
        steps = 0

        k = 0
        for zone_r in range(0, 9, 3):
            for zone_c in range(0, 9, 3):
                r = zone_r + random.randint(0, 2)
                c = zone_c + random.randint(0, 2)
                matrix[r][c] = k
                sizes[k] = 1
                k += 1

        if fill(matrix, sizes):
            return matrix