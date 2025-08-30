import pygame
import os


def _default_sound_dir() -> str:
    return os.path.abspath(
        os.path.join(os.path.dirname(__file__), os.pardir, "sounds")
    )


def load_sounds(sound_dir: str | None = None):
    """
    Load the sound effects for the game.

    Args:
        sound_dir: The directory where the sound files are stored.

    Returns:
        A dictionary of the loaded sound objects.
    """
    pygame.mixer.init()

    if sound_dir is None:
        sound_dir = _default_sound_dir()

    sounds: dict[str, pygame.mixer.Sound] = {}
    if not os.path.exists(sound_dir):
        print(f"Warning: Sound directory '{sound_dir}' not found.")
        return sounds
        
    SUPPORTED_EXTENSIONS = ('.wav', '.mp3', '.ogg')

    for filename in os.listdir(sound_dir):
        if filename.lower().endswith(SUPPORTED_EXTENSIONS):
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

