from collections import Counter, deque
import random
from typing import Deque, List

# Move constants
MOVES: List[str] = ['rock', 'paper', 'scissors']

# Map a move to the move that beats it
COUNTER_MOVE = {
    'rock': 'paper',
    'paper': 'scissors',
    'scissors': 'rock',
}


def _most_common_move(history: Deque[str]) -> str:
    """Return the most frequent move in *history* (random tie-break)."""
    if not history:
        return random.choice(MOVES)
    frequency = Counter(history)
    top_moves = frequency.most_common()
    if len(top_moves) == 1 or top_moves[0][1] > top_moves[1][1]:
        return top_moves[0][0]
    max_count = top_moves[0][1]
    tied = [mv for mv, cnt in top_moves if cnt == max_count]
    return random.choice(tied)


def _predict_next_move_markov(history: Deque[str]) -> str:
    """First-order Markov prediction for the player's next move."""
    if len(history) < 2:
        return _most_common_move(history)

    transitions = {mv: Counter() for mv in MOVES}
    last = None
    for mv in history:
        if last is not None:
            transitions[last][mv] += 1
        last = mv

    current = history[-1]
    if not transitions[current]:
        return _most_common_move(history)

    candidates = transitions[current].most_common()
    max_count = candidates[0][1]
    top = [mv for mv, cnt in candidates if cnt == max_count]
    return random.choice(top)


def smart_choice(history: Deque[str] | None = None, difficulty: str = 'medium') -> str:
    """Return the computer's move based on difficulty.

    Difficulty levels:
    • easy   – random
    • medium – counters the most common player move
    • hard   – Markov prediction + counter
    """
    difficulty = difficulty.lower()
    if difficulty not in {'easy', 'medium', 'hard'}:
        raise ValueError(f'Unknown difficulty: {difficulty}')

    if history is None or difficulty == 'easy':
        return random.choice(MOVES)

    if difficulty == 'medium':
        predicted = _most_common_move(history)
    else:
        predicted = _predict_next_move_markov(history)

    return COUNTER_MOVE[predicted]
