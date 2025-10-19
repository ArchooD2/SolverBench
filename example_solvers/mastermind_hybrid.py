"""
Mastermind Solver (Hybrid Fast-Entropy, Debug Version)
------------------------------------------------------
Adds detailed debug prints to trace candidate counts,
branch decisions, and entropy sampling each iteration.
"""

import itertools
import random
from typing import List
from collections import defaultdict
from puzzles.mastermind import COLORS, CODE_LENGTH, MastermindSession, peg_feedback
from core.registry import register_solver

ALL_CODES = ["".join(p) for p in itertools.product(COLORS, repeat=CODE_LENGTH)]

@register_solver("mastermind", "hybrid")
def solve_mastermind(session: MastermindSession) -> List[str]:
    candidates = ALL_CODES.copy()
    guesses: List[str] = []

    def sample_entropy(guess: str, pool: List[str], sample_size: int = 80):
        """Estimate entropy by sampling from the candidate pool only."""
        if not pool:
            return 0.0
        if len(pool) <= sample_size:
            sample = pool
        else:
            sample = random.sample(pool, sample_size)
        partitions = defaultdict(int)
        for code in sample:
            partitions[peg_feedback(guess, code)] += 1
        total = len(sample)
        if total == 0:
            return 0.0
        entropy = -sum((count / total) ** 2 for count in partitions.values())
        return entropy

    current_guess = random.choice(candidates)

    while len(guesses) < session.max_guesses:
        guesses.append(current_guess)
        blacks, whites = session.guess(current_guess)

        if blacks == CODE_LENGTH:
            break

        # keep only codes consistent with current feedback
        old_len = len(candidates)
        candidates = [
            code for code in candidates
            if peg_feedback(current_guess, code) == (blacks, whites)
        ]

        if not candidates:
            break

        if len(candidates) <= 10:
            # small pool → random elimination is fine
            current_guess = random.choice(candidates)
        else:
            # score a small random subset of *candidates*
            subset_size = min(60, len(candidates))
            options = random.sample(candidates, subset_size)
            scored = [(sample_entropy(g, candidates), g) for g in options]
            current_guess = max(scored, key=lambda x: x[0])[1]

    return guesses
