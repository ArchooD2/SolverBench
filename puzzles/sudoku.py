"""
Sudoku Puzzle Definition
------------------------
Generates solved Sudoku boards and removes cells to create puzzles.
"""

from typing import List, Optional
import random

Board = List[List[int]]

# ----------------------------------------------------------------------
# Basic Sudoku utilities
# ----------------------------------------------------------------------
def is_valid(board: Board, row: int, col: int, num: int) -> bool:
    if num in board[row]:
        return False
    if num in [board[r][col] for r in range(9)]:
        return False
    start_r, start_c = (row // 3) * 3, (col // 3) * 3
    for r in range(start_r, start_r + 3):
        for c in range(start_c, start_c + 3):
            if board[r][c] == num:
                return False
    return True


def find_empty(board: Board) -> Optional[tuple[int, int]]:
    for r in range(9):
        for c in range(9):
            if board[r][c] == 0:
                return r, c
    return None


# ----------------------------------------------------------------------
# Generator: build a complete solved board using backtracking
# ----------------------------------------------------------------------
def _fill_board(board: Board) -> bool:
    empty = find_empty(board)
    if not empty:
        return True
    row, col = empty
    nums = list(range(1, 10))
    random.shuffle(nums)
    for num in nums:
        if is_valid(board, row, col, num):
            board[row][col] = num
            if _fill_board(board):
                return True
            board[row][col] = 0
    return False


def generate_solved_board(seed: Optional[int] = None) -> Board:
    if seed is not None:
        random.seed(seed)
    board = [[0 for _ in range(9)] for _ in range(9)]
    _fill_board(board)
    return board


# ----------------------------------------------------------------------
# Puzzle creator: remove numbers while keeping a solvable puzzle
# ----------------------------------------------------------------------
def make_puzzle(board: Board, holes: int = 40) -> Board:
    puzzle = [row[:] for row in board]
    positions = [(r, c) for r in range(9) for c in range(9)]
    random.shuffle(positions)
    for i in range(min(holes, 81)):
        r, c = positions[i]
        puzzle[r][c] = 0
    return puzzle


# ----------------------------------------------------------------------
# Convenience wrappers for benchmarking
# ----------------------------------------------------------------------
def generate_dataset(n: int = 3, holes: int = 40) -> tuple[list[Board], list[Board]]:
    """Return (puzzles, solutions) pair lists."""
    puzzles, solutions = [], []
    for i in range(n):
        solved = generate_solved_board()
        puzzle = make_puzzle(solved, holes)
        puzzles.append(puzzle)
        solutions.append(solved)
    return puzzles, solutions

# ----------------------------------------------------------------------
# Accuracy function for Sudoku
# ----------------------------------------------------------------------
def sudoku_accuracy(output, reference):
    # Require complete, valid board, not necessarily identical.
    from puzzles.sudoku import find_empty, is_valid
    if find_empty(output) is not None:
        return 0.0
    for r in range(9):
        for c in range(9):
            if not is_valid(output, r, c, output[r][c]):
                return 0.0
    # Optionally completed board, can be different from reference.
    return 1.0


from core.registry import register_puzzle
register_puzzle("sudoku", accuracy_fn=sudoku_accuracy)