"""
Mastermind Solver (Elimination, GameSession-based)
---------------------------------------------------
Constraint-based approach using feedback-only GameSession.
"""

import itertools
import random
from copy import deepcopy
from typing import List
from puzzles.mastermind import COLORS, CODE_LENGTH, MastermindSession, peg_feedback
from core.registry import register_solver

ALL_CODES = ["".join(p) for p in itertools.product(COLORS, repeat=CODE_LENGTH)]

@register_solver("mastermind", "elimination")
def solve_mastermind(session: MastermindSession) -> List[str]:
    candidates = deepcopy(ALL_CODES)
    guesses: List[str] = []

    current_guess = random.choice(candidates)

    while len(guesses) < session.max_guesses:
        guesses.append(current_guess)
        blacks, whites = session.guess(current_guess)
        if blacks == CODE_LENGTH:
            break

        candidates = [
            code for code in candidates
            if peg_feedback(current_guess, code) == (blacks, whites)
        ]


        if not candidates:
            break
        current_guess = random.choice(candidates)

    return guesses
