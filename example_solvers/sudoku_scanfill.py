"""
Example Sudoku Solver (Scan-Fill)
---------------------------------
Fills cells that have only one valid option, repeating until stuck.
This isn't guaranteed to solve all puzzles, but it's very fast for easy ones.
"""

from copy import deepcopy
from core.registry import register_solver
from puzzles.sudoku import is_valid, find_empty, Board


@register_solver("sudoku", "scanfill")
def solve_scanfill(board: Board):
    board = deepcopy(board)

    progress = True
    while progress:
        progress = False
        for r in range(9):
            for c in range(9):
                if board[r][c] == 0:
                    possible = [n for n in range(1, 10) if is_valid(board, r, c, n)]
                    if len(possible) == 1:
                        board[r][c] = possible[0]
                        progress = True

        # stop if fully filled
        if not any(0 in row for row in board):
            return board

    # fallback: partially solved or unsolved
    return board
