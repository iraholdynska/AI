import unittest
from solver import count_solutions

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


class TestSolver(unittest.TestCase):
    def test_unique_solution(self):
        board = [row[:] for row in SOLVED]
        board[0][0] = 0
        board[0][1] = 0
        self.assertEqual(count_solutions(board, REGIONS), 1)

    def test_multiple_solutions(self):
        empty = [[0] * 9 for _ in range(9)]
        self.assertEqual(count_solutions(empty, REGIONS, limit=2), 2)


if __name__ == "__main__":
    unittest.main()