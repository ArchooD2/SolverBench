"""
Example Sudoku Solver (Backtracking)
------------------------------------
Classic recursive solver using the registry system.
"""

from copy import deepcopy
from core.registry import register_solver
from puzzles.sudoku import is_valid, find_empty, Board


@register_solver("sudoku", "backtracking")
def solve_sudoku(board: Board):
    board = deepcopy(board)
    if _solve(board):
        return board
    return None


def _solve(board: Board) -> bool:
    """Recursive backtracking helper."""
    empty = find_empty(board)
    if not empty:
        return True  # solved
    row, col = empty

    for num in range(1, 10):
        if is_valid(board, row, col, num):
            board[row][col] = num
            if _solve(board):
                return True
            board[row][col] = 0

    return False
