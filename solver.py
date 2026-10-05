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