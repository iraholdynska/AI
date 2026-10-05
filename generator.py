import random
from solver import count_solutions, get_candidates
from regions import generate_regions

max_fill_steps = 5000
fill_steps = 0


def fill_matrix(matrix, regions):
    global fill_steps
    fill_steps += 1
    if fill_steps > max_fill_steps:
        return False

    best_cell = None
    min_cand_len = 10
    best_cand = []

    for r in range(9):
        for c in range(9):
            if matrix[r][c] == 0:
                cand = get_candidates(matrix, regions, r, c)
                if not cand:
                    return False
                if len(cand) < min_cand_len:
                    min_cand_len = len(cand)
                    best_cell = (r, c)
                    best_cand = cand

    if best_cell is None:
        return True

    r, c = best_cell
    random.shuffle(best_cand)

    for num in best_cand:
        matrix[r][c] = num
        if fill_matrix(matrix, regions):
            return True
        matrix[r][c] = 0

    return False


def remove_numbers(matrix, regions, target):
    cells = [(r, c) for r in range(9) for c in range(9)]
    random.shuffle(cells)
    removed = 0

    for r, c in cells:
        if removed >= target:
            break

        backup = matrix[r][c]
        matrix[r][c] = 0

        if count_solutions(matrix, regions, limit=2) == 1:
            removed += 1
        else:
            matrix[r][c] = backup

    return removed


def generate_puzzle(target):
    global fill_steps

    while True:
        regions = generate_regions()
        matrix = [[0] * 9 for _ in range(9)]
        fill_steps = 0

        if fill_matrix(matrix, regions):
            break

    solution = [row[:] for row in matrix]
    remove_numbers(matrix, regions, target)
    return matrix, solution, regions