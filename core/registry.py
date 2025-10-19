"""
SolverBench Registry
--------------------
Handles dynamic registration and retrieval of solvers.

Each solver is registered with:
    @register_solver(puzzle="sudoku", name="backtracking")
    def solve_sudoku(...): ...

Internally stores solvers as:
    _registry = {
        "sudoku": {
            "backtracking": <function>,
            "constraint": <function>,
        },
        "pathfinding": {
            "bfs": <function>,
        }
    }
"""

from typing import Callable, Dict

# main registry structure
_registry: Dict[str, Dict[str, Callable]] = {}
_puzzles: dict[str, dict] = {}

def register_puzzle(name: str, accuracy_fn=None):
    """Register a puzzle type and its optional accuracy function."""
    def decorator(cls_or_func):
        _puzzles[name] = {"accuracy": accuracy_fn}
        return cls_or_func
    return decorator

def get_accuracy_fn(puzzle: str):
    entry = _puzzles.get(puzzle, {})
    return entry.get("accuracy")

def register_solver(puzzle: str, name: str):
    """
    Decorator to register a solver function.
    Example:
        @register_solver("sudoku", "backtracking")
        def solve(board): ...
    """
    def decorator(func: Callable):
        if puzzle not in _registry:
            _registry[puzzle] = {}
        if name in _registry[puzzle]:
            raise ValueError(f"Solver '{name}' for puzzle '{puzzle}' already exists.")
        _registry[puzzle][name] = func
        return func
    return decorator


def get_solver(puzzle: str, name: str) -> Callable:
    """Retrieve a solver by puzzle and name."""
    try:
        return _registry[puzzle][name]
    except KeyError:
        raise ValueError(f"Solver '{name}' not found for puzzle '{puzzle}'.")


def list_puzzles() -> list[str]:
    """List all puzzles currently registered."""
    return list(_registry.keys())


def list_solvers(puzzle: str) -> list[str]:
    """List all solvers available for a specific puzzle."""
    return list(_registry.get(puzzle, {}).keys())


def all_solvers() -> Dict[str, Dict[str, Callable]]:
    """Return the entire registry (read-only)."""
    return {p: dict(s) for p, s in _registry.items()}
