import unittest
from validator import find_conflicts, is_solved

REGIONS = [[(r // 3) * 3 + c // 3 for c in range(9)] for r in range(9)]

SOLVED = [
    [5, 3, 4, 6, 7, 8, 9, 1, 2],
    [6, 7, 2, 1, 9, 5, 3, 4, 8],
    [1, 9, 8, 3, 4, 2, 5, 6, 7],
    [8, 5, 9, 7, 6, 1, 4, 2, 3],
    [4, 2, 6, 8, 5, 3, 7, 9, 1],
    [7, 1, 3, 9, 2, 4, 8, 5, 6],
    [9, 6, 1, 5, 3, 7, 2, 8, 4],
    [2, 8, 7, 4, 1, 9, 6, 3, 5],
    [3, 4, 5, 2, 8, 6, 1, 7, 9],
]


def copy(board):
    return [row[:] for row in board]


class TestValidator(unittest.TestCase):
    def test_solved_board(self):
        self.assertEqual(find_conflicts(copy(SOLVED), REGIONS), set())
        self.assertTrue(is_solved(copy(SOLVED), REGIONS))

    def test_incomplete_board(self):
        board = copy(SOLVED)
        board[0][0] = 0
        self.assertEqual(find_conflicts(board, REGIONS), set())
        self.assertFalse(is_solved(board, REGIONS))

    def test_row_conflict(self):
        board = copy(SOLVED)
        board[0][0] = board[0][1]
        self.assertEqual(find_conflicts(board, REGIONS) & {(0, 0), (0, 1)}, {(0, 0), (0, 1)})
        self.assertFalse(is_solved(board, REGIONS))

    def test_column_conflict(self):
        board = copy(SOLVED)
        board[0][0] = board[8][0]
        self.assertEqual(find_conflicts(board, REGIONS) & {(0, 0), (8, 0)}, {(0, 0), (8, 0)})

    def test_region_conflict(self):
        board = [[0] * 9 for _ in range(9)]
        board[0][0] = 7
        board[2][2] = 7
        self.assertEqual(find_conflicts(board, REGIONS), {(0, 0), (2, 2)})

    def test_no_false_conflict(self):
        board = [[0] * 9 for _ in range(9)]
        board[0][0] = 7
        board[4][4] = 7
        self.assertEqual(find_conflicts(board, REGIONS), set())


if __name__ == "__main__":
    unittest.main()