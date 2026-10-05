def same_group(regions, r1, c1, r2, c2):
    return r1 == r2 or c1 == c2 or regions[r1][c1] == regions[r2][c2]


def find_conflicts(matrix, regions):
    conflicts = set()
    for r in range(9):
        for c in range(9):
            if matrix[r][c] == 0:
                continue
            for i in range(9):
                for j in range(9):
                    if (i, j) == (r, c):
                        continue
                    if matrix[i][j] == matrix[r][c] and same_group(regions, r, c, i, j):
                        conflicts.add((r, c))
                        conflicts.add((i, j))
    return conflicts


def is_solved(matrix, regions):
    for row in matrix:
        if 0 in row:
            return False
    return len(find_conflicts(matrix, regions)) == 0