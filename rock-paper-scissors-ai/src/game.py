import random

def get_computer_choice():
    """Randomly select rock, paper, or scissors for the computer."""
    return random.choice(['rock', 'paper', 'scissors'])

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
