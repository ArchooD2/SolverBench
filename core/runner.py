"""
SolverBench Runner
------------------
Executes registered solvers with standardized benchmarking and reporting.

Handles:
- Fetching solvers from registry
- Timing execution
- (Optional) memory measurement
- Validating output if a reference solution is available
"""

import copy
import time
import tracemalloc
from typing import Any, Callable, Dict, Optional

from core.registry import get_solver
from core import metrics


def run_single(puzzle: str, solver_name: str, input_data: Any,
               reference_output: Optional[Any] = None,
               measure_memory: bool = False) -> Dict[str, Any]:
    """
    Run a single solver once and collect metrics.

    Args:
        puzzle: the puzzle name ("sudoku", "pathfinding", etc.)
        solver_name: the registered solver to use
        input_data: data to solve (puzzle board, graph, etc.)
        reference_output: optional known correct result for validation
        measure_memory: whether to use tracemalloc

    Returns:
        dict with runtime info, success, output, and stats
    """
    solver = get_solver(puzzle, solver_name)
    result = {"puzzle": puzzle, "solver": solver_name}
    
    # measure performance
    if measure_memory:
        tracemalloc.start()

    start_time = time.perf_counter()
    try:
        output = solver(input_data)
        success = True
    except Exception as e:
        output = e
        success = False
    elapsed = (time.perf_counter() - start_time) * 1000  # ms

    if measure_memory:
        current, peak = tracemalloc.get_traced_memory()
        tracemalloc.stop()
    else:
        current = peak = None

    # compute correctness metric (if reference provided)
    accuracy = None
    if reference_output is not None and success:
        from core.registry import get_accuracy_fn
        acc_fn = get_accuracy_fn(puzzle)
        if reference_output is not None and success:
            if acc_fn:
                accuracy = acc_fn(output, reference_output)
            else:
                accuracy = metrics.compute_accuracy(output, reference_output)


    result.update({
        "success": success,
        "time_ms": round(elapsed, 3),
        "mem_peak": peak,
        "accuracy": accuracy,
        "output": output,
    })
    return result


def run_batch(puzzle: str, solver_names, dataset, references=None, measure_memory=False):
    """
    Run each solver on each input in the dataset, returning a flat result list.
    """
    results = []
    for i, solver_name in enumerate(solver_names):
        print(f"[SolverBench] Running solver '{solver_name}' on puzzle '{puzzle}'...")
        for j, input_case in enumerate(dataset):
            ref = references[j] if references and j < len(references) else None

            fresh_input = copy.deepcopy(input_case)
            res = run_single(puzzle, solver_name, fresh_input, ref, measure_memory)
            res["case_index"] = j
            results.append(res)
    return results