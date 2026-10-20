def get_candidates(matrix, regions, r, c):
    if matrix[r][c] != 0:
        return []
    used = set(matrix[r])
    for i in range(9):
        used.add(matrix[i][c])
    k = regions[r][c]
    for i in range(9):
        for j in range(9):
            if regions[i][j] == k and matrix[i][j] != 0:
                used.add(matrix[i][j])
    return [num for num in range(1, 10) if num not in used]


def find_best_empty_cell(matrix, regions):
    best_cell = None
    min_candidates = 10

    for r in range(9):
        for c in range(9):
            if matrix[r][c] == 0:
                candidates = get_candidates(matrix, regions, r, c)
                count = len(candidates)
                if count == 0:
                    return (r, c), []
                if count < min_candidates:
                    min_candidates = count
                    best_cell = ((r, c), candidates)
                    if min_candidates == 1:
                        return best_cell

    return best_cell if best_cell else (None, [])


def count_solutions(matrix, regions, limit=2):
    cell_info = find_best_empty_cell(matrix, regions)
    if cell_info[0] is None:
        return 1

    (r, c), candidates = cell_info
    if not candidates:
        return 0

    count = 0
    for num in candidates:
        matrix[r][c] = num
        count += count_solutions(matrix, regions, limit)
        matrix[r][c] = 0
        if count >= limit:
            return count

    return count


def get_units(regions):
    rows = [("рядку", [(r, c) for c in range(9)]) for r in range(9)]
    cols = [("стовпці", [(r, c) for r in range(9)]) for c in range(9)]
    areas = [("області", [(r, c) for r in range(9) for c in range(9) if regions[r][c] == k]) 
             for k in range(9)]
    return rows + cols + areas


def find_logical_step(matrix, regions):
    for r in range(9):
        for c in range(9):
            candidates = get_candidates(matrix, regions, r, c)
            if len(candidates) == 1:
                return r, c, candidates[0], "це єдина можлива цифра для клітинки"
    for name, cells in get_units(regions):
        for num in range(1, 10):
            if any(matrix[r][c] == num for r, c in cells):
                continue
            places = [(r, c) for r, c in cells 
                      if matrix[r][c] == 0 and num in get_candidates(matrix, regions, r, c)]
            if len(places) == 1:
                r, c = places[0]
                return r, c, num, f"цифра {num} може стояти у {name} лише тут"
    return None


def find_guess_step(matrix, regions):
    (r, c), candidates = find_best_empty_cell(matrix, regions)
    if r is None:
        return None
    for num in candidates:
        matrix[r][c] = num
        solvable = count_solutions(matrix, regions, 1)
        matrix[r][c] = 0
        if solvable:
            return r, c, num, "логічних кроків немає, цифру підібрано перебором"
    return None


def solve_steps(matrix, regions):
    work = [row[:] for row in matrix]
    while True:
        step = find_logical_step(work, regions) or find_guess_step(work, regions)
        if step is None:
            return
        r, c, num, _ = step
        work[r][c] = num
        yield step