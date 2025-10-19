from puzzles.sudoku import EXAMPLE_PUZZLES, EXAMPLE_SOLUTIONS
from core.runner import run_single
import example_solvers.sudoku_backtracking  # ensures solver registers

board = EXAMPLE_PUZZLES[0]
solution = EXAMPLE_SOLUTIONS[0]

res = run_single("sudoku", "backtracking", board, reference_output=solution)
print(res)
