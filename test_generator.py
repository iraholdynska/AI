import unittest
from solver import count_solutions
from generator import generate_puzzle


class TestGenerator(unittest.TestCase):
    def test_generated_puzzle(self):
        target = 35
        puzzle, solution, regions = generate_puzzle(target)

        zeros = sum(row.count(0) for row in puzzle)
        self.assertEqual(zeros, target)

        for r in range(9):
            for c in range(9):
                self.assertIn(puzzle[r][c], (0, solution[r][c]))

        self.assertEqual(count_solutions([row[:] for row in puzzle], regions), 1)


if __name__ == "__main__":
    unittest.main()