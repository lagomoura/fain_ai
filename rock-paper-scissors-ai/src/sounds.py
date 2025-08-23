import pygame
import os

def load_sounds(sound_dir='rock-paper-scissors-ai/sounds'):
    """
    Load the sound effects for the game.

    Args:
        sound_dir: The directory where the sound files are stored.

    Returns:
        A dictionary of the loaded sound objects.
    """
    pygame.mixer.init()
    sounds = {}
    if not os.path.exists(sound_dir):
        print(f"Warning: Sound directory '{sound_dir}' not found.")
        return sounds
        
    for filename in os.listdir(sound_dir):
        if filename.endswith('.wav'):
            name = os.path.splitext(filename)[0]
            path = os.path.join(sound_dir, filename)
            try:
                sounds[name] = pygame.mixer.Sound(path)
            except pygame.error as e:
                print(f"Warning: Could not load sound '{path}': {e}")
    return sounds

def play_sound(sound):
    """
    Play a sound effect.

    Args:
        sound: The sound object to play.
    """
    if sound:
        sound.play()

