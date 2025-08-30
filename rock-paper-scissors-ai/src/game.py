# New smart AI integration
from collections import deque
from typing import Deque, Optional

from .ai import smart_choice


def get_computer_choice(
    history: Optional[Deque[str]] = None,
    difficulty: str = "medium",
) -> str:
    """Return the computer's move based on the selected *difficulty*.

    The function remains backward-compatible: when *history* is ``None`` it
    falls back to a random choice (equivalent to *easy*).
    """

    return smart_choice(history, difficulty)

def get_winner(player_choice, computer_choice):
    """
    Determine the winner of a rock-paper-scissors game.

    Args:
        player_choice: The player's choice ('rock', 'paper', or 'scissors').
        computer_choice: The computer's choice ('rock', 'paper', or 'scissors').

    Returns:
        The winner ('player', 'computer', or 'tie').
    """
    if player_choice == computer_choice:
        return 'tie'
    elif (player_choice == 'rock' and computer_choice == 'scissors') or \
         (player_choice == 'scissors' and computer_choice == 'paper') or \
         (player_choice == 'paper' and computer_choice == 'rock'):
        return 'player'
    else:
        return 'computer'
