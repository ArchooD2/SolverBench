"""
SolverBench CLI
---------------
Run benchmarks and comparisons from the command line.

Usage:
    python cli.py benchmark sudoku --solver backtracking
    python cli.py benchmark sudoku --all
    python cli.py benchmark sudoku --import mysolver.py --solver mysolver
"""

import sys
import os
import importlib.util
import importlib
import pkgutil
from typing import List
from core.registry import get_accuracy_fn
from core.runner import run_batch
from core.registry import list_solvers
from core.metrics import summarize_results
from puzzles import sudoku
import example_solvers


# ---------------------------------------------------------------------------
# Internal solver auto-loader
# ---------------------------------------------------------------------------
def autoload_internal_solvers():
    """Auto-import all solvers bundled in example_solvers/"""
    for _, modname, _ in pkgutil.iter_modules(example_solvers.__path__):
        importlib.import_module(f"example_solvers.{modname}")


# ---------------------------------------------------------------------------
# External solver loader (user-supplied)
# ---------------------------------------------------------------------------
def import_extra_modules(paths):
    """Import arbitrary modules or .py files specified by the user."""
    for path in paths or []:
        if os.path.isfile(path) and path.endswith(".py"):
            modname = os.path.splitext(os.path.basename(path))[0]
            spec = importlib.util.spec_from_file_location(modname, path)
            module = importlib.util.module_from_spec(spec)
            sys.modules[modname] = module
            spec.loader.exec_module(module)
            print(f"[SolverBench] Imported file: {path}")
        else:
            importlib.import_module(path)
            print(f"[SolverBench] Imported module: {path}")


# ---------------------------------------------------------------------------
# SnapArg detection
# ---------------------------------------------------------------------------
use_snaparg = False
if importlib.util.find_spec("snaparg") is not None:
    import snaparg
    use_snaparg = True
else:
    import argparse


# ---------------------------------------------------------------------------
# Common benchmark logic
# ---------------------------------------------------------------------------
def run_benchmark(puzzle: str, solvers: List[str], measure_memory=False):
    """Run solvers on the given puzzle dataset."""

    # Try to dynamically import the puzzle module
    try:
        puzzle_module = __import__(f"puzzles.{puzzle}", fromlist=[""])
    except ModuleNotFoundError:
        print(f"[ERROR] Puzzle module 'puzzles.{puzzle}' not found.")
        sys.exit(1)

    # Try to call the dataset generator
    try:
        dataset, refs = puzzle_module.generate_dataset()
    except AttributeError:
        print(f"[ERROR] Puzzle '{puzzle}' does not define generate_dataset().")
        sys.exit(1)

    results = run_batch(
        puzzle, solvers, dataset, references=refs, measure_memory=measure_memory
    )
    print(summarize_results(results))

# ---------------------------------------------------------------------------
# SnapArg CLI
# ---------------------------------------------------------------------------
def cli_snaparg():
    parser = snaparg.SnapArgumentParser(description="SolverBench CLI (SnapArg-powered)")

    parser.add_argument("command", choices=["benchmark"], help="Command to execute.")
    parser.add_argument("puzzle", help="Puzzle name (e.g., sudoku).")
    parser.add_argument("--solver", help="Specific solver name.")
    parser.add_argument("--all", action="store_true", help="Run all solvers for the puzzle.")
    parser.add_argument("--memory", action="store_true", help="Track memory usage.")
    parser.add_argument("--autofix", action="store_true", help="Auto-fix argument typos.")
    parser.add_argument(
        "--import",
        dest="extra_modules",
        nargs="+",
        help="Additional modules or .py files to import before running.",
    )

    args = parser.parse_args()

    # load solvers
    autoload_internal_solvers()
    import_extra_modules(getattr(args, "extra_modules", []))

    if args.command == "benchmark":
        available = list_solvers(args.puzzle)
        if args.all:
            solvers = available
        elif args.solver:
            solvers = [args.solver]
        else:
            print("[ERROR] Must specify --solver or --all")
            sys.exit(1)

        run_benchmark(args.puzzle, solvers, measure_memory=args.memory)


# ---------------------------------------------------------------------------
# Argparse CLI fallback
# ---------------------------------------------------------------------------
def cli_argparse():
    import argparse

    parser = argparse.ArgumentParser(description="SolverBench CLI (fallback mode)")
    parser.add_argument("command", choices=["benchmark"], help="Command to run")
    parser.add_argument("puzzle", help="Puzzle name (e.g., sudoku)")
    parser.add_argument("--solver", help="Specific solver to run")
    parser.add_argument("--all", action="store_true", help="Run all solvers for the puzzle")
    parser.add_argument("--memory", action="store_true", help="Track memory usage")
    parser.add_argument(
        "--import",
        dest="extra_modules",
        nargs="+",
        help="Additional modules or .py files to import before running.",
    )

    args = parser.parse_args()

    # load solvers
    autoload_internal_solvers()
    import_extra_modules(getattr(args, "extra_modules", []))

    if args.command == "benchmark":
        available = list_solvers(args.puzzle)
        if args.all:
            solvers = available
        elif args.solver:
            solvers = [args.solver]
        else:
            print("[ERROR] Must specify --solver or --all")
            sys.exit(1)

        run_benchmark(args.puzzle, solvers, measure_memory=args.memory)


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    print(f"[SolverBench CLI] Using {'SnapArg' if use_snaparg else 'argparse'} parser.\n")
    (cli_snaparg if use_snaparg else cli_argparse)()
