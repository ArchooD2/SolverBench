"""
SolverBench Metrics
-------------------
Provides accuracy and comparison utilities for solver outputs.

Currently supports:
- direct equality comparison
- numeric tolerance comparison (for floats, vectors, etc.)
"""
from statistics import mean
from typing import Any, Union

def compute_accuracy(output: Any, reference: Any, tolerance: float = 1e-9) -> Union[float, None]:
    """
    Compare solver output to a reference solution.

    Returns:
        - 1.0 if exactly equal
        - 0.0 if not equal
        - or a fractional score (for numeric closeness)
        - None if comparison is not meaningful
    """
    # handle basic equality
    if output == reference:
        return 1.0

    # handle numeric closeness
    if isinstance(output, (int, float)) and isinstance(reference, (int, float)):
        diff = abs(output - reference)
        return max(0.0, 1.0 - diff / (abs(reference) + tolerance))

    # handle sequence comparison (e.g. list of numbers)
    if isinstance(output, list) and isinstance(reference, list) and len(output) == len(reference):
        matches = sum(
            1 if compute_accuracy(o, r, tolerance) >= 0.999 else 0
            for o, r in zip(output, reference)
        )
        return matches / len(reference)

    # if can't compare meaningfully
    return None


def summarize_results(results: list[dict]) -> str:
    """
    Produce a readable grouped summary by solver.
    """
    if not results:
        return "No results."

    # group by solver
    grouped = {}
    for r in results:
        solver = r["solver"]
        grouped.setdefault(solver, []).append(r)

    lines = []
    for solver, group in grouped.items():
        success_count = sum(1 for r in group if r["success"])
        acc_values = [r["accuracy"] for r in group if r.get("accuracy") is not None]
        time_values = [r["time_ms"] for r in group]
        acc_avg = mean(acc_values) if acc_values else 0.0

        line = (
            f"SolverBench Summary — {group[0]['puzzle']} / {solver} ({len(group)} cases)\n"
            f"{'-'*54}\n"
            f"✓ {success_count} runs, {success_count/len(group)*100:.1f}% success\n"
            f"⏱ avg time: {mean(time_values):.2f} ms   "
            f"min: {min(time_values):.2f} ms   max: {max(time_values):.2f} ms\n"
            f"🎯 avg accuracy: {acc_avg*100:.1f}%\n"
        )
        lines.append(line)

    return "\n".join(lines)