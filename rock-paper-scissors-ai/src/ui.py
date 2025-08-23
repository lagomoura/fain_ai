import cv2
import numpy as np

def overlay_image(background, overlay, x, y):
    """
    Overlay a transparent image on a background.

    Args:
        background: The background image.
        overlay: The overlay image (with transparency).
        x: The x-coordinate to place the overlay.
        y: The y-coordinate to place the overlay.
    """
    h, w, _ = overlay.shape
    
    # Extract the alpha channel
    alpha = overlay[:, :, 3] / 255.0
    
    # Extract the RGB channels
    rgb = overlay[:, :, :3]

    # Blend the images
    for c in range(0, 3):
        background[y:y+h, x:x+w, c] = (
            alpha * rgb[:, :, c] +
            background[y:y+h, x:x+w, c] * (1.0 - alpha)
        )

def display_ui(image, player_choice, computer_choice, winner, scores, images):
    """
    Display the game UI on the image.

    Args:
        image: The image to draw on.
        player_choice: The player's choice.
        computer_choice: The computer's choice.
        winner: The winner of the round.
        scores: A dictionary with the scores for the player and computer.
        images: A dictionary of the game images.
    """
    # Display the player's choice image
    if player_choice in images:
        player_img = images[player_choice]
        overlay_image(image, player_img, 50, 50)

    # Display the computer's choice image
    if computer_choice in images:
        computer_img = images[computer_choice]
        overlay_image(image, computer_img, image.shape[1] - 150, 50)

    # Display the winner
    cv2.putText(
        image,
        f'Winner: {winner}',
        (50, 200),
        cv2.FONT_HERSHEY_SIMPLEX,
        1,
        (0, 255, 0) if winner == 'player' else (0, 0, 255),
        2,
        cv2.LINE_AA,
    )

    # Display the scores
    cv2.putText(
        image,
        f"Scores - You: {scores['player']} | AI: {scores['computer']}",
        (50, 250),
        cv2.FONT_HERSHEY_SIMPLEX,
        1,
        (255, 255, 255),
        2,
        cv2.LINE_AA,
    )
