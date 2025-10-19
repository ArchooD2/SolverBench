"""
Mastermind Puzzle Definition (Self-contained)
---------------------------------------------
Encapsulates dataset generation, GameSession logic, and accuracy.
"""

import random
from typing import List, Tuple
from core.registry import register_puzzle

# Configuration
COLORS = ["R", "G", "B", "Y", "P", "O"]
CODE_LENGTH = 4
MAX_GUESSES = 6


# ----------------------------------------------------------------------
# Feedback Logic
# ----------------------------------------------------------------------
def peg_feedback(guess: str, secret: str) -> Tuple[int, int]:
    """Compute Mastermind-style feedback (black and white pegs)."""
    blacks = sum(g == s for g, s in zip(guess, secret))
    guess_colors = {c: guess.count(c) for c in COLORS}
    secret_colors = {c: secret.count(c) for c in COLORS}
    total_color_matches = sum(min(guess_colors[c], secret_colors[c]) for c in COLORS)
    whites = total_color_matches - blacks
    return blacks, whites


# ----------------------------------------------------------------------
# GameSession Class
# ----------------------------------------------------------------------
class MastermindSession:
    """Encapsulates the state and feedback for a single Mastermind game."""
    def __init__(self, secret: str = None, max_guesses: int = MAX_GUESSES):
        self.secret = secret or "".join(random.choices(COLORS, k=CODE_LENGTH))
        self.max_guesses = max_guesses
        self.history = []

    def guess(self, attempt: str) -> Tuple[int, int]:
        """Submit a guess and receive (blacks, whites) feedback."""
        if len(self.history) >= self.max_guesses:
            raise Exception("Max guesses exceeded.")
        feedback = peg_feedback(attempt, self.secret)
        self.history.append((attempt, feedback))
        return feedback


# ----------------------------------------------------------------------
# Dataset Generator
# ----------------------------------------------------------------------
def generate_dataset(n: int = 45) -> Tuple[List[MastermindSession], List[str]]:
    """Generate n random Mastermind sessions and their corresponding secrets."""
    sessions = [MastermindSession() for _ in range(n)]
    refs = [s.secret for s in sessions]
    return sessions, refs


# ----------------------------------------------------------------------
# Accuracy Function
# ----------------------------------------------------------------------
def mastermind_accuracy(output: List[str], reference: str) -> float:
    """Compute accuracy: 1.0 if reference appears in guess list, else 0.0."""
    if not output or not isinstance(output, list):
        return 0.0
    return 1.0 if reference in output else 0.0


# ----------------------------------------------------------------------
# Puzzle Registration
# ----------------------------------------------------------------------
@register_puzzle("mastermind", accuracy_fn=mastermind_accuracy)
class _MastermindPuzzle:
    """Sentinel class to trigger decorator-based registration."""
    pass
