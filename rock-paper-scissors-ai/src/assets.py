import cv2
import os

def load_images(asset_dir='rock-paper-scissors-ai/assets'):
    """
    Load and resize the images for the game.

    Args:
        asset_dir: The directory where the images are stored.

    Returns:
        A dictionary of the loaded images.
    """
    images = {}
    for filename in os.listdir(asset_dir):
        if filename.endswith('.png'):
            name = os.path.splitext(filename)[0]
            path = os.path.join(asset_dir, filename)
            image = cv2.imread(path, cv2.IMREAD_UNCHANGED)
            if image is not None:
                images[name] = cv2.resize(image, (100, 100))
    return images
