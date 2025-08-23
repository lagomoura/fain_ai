import cv2
import time

def display_winner_animation(image, winner):
    """
    Display a winner animation on the image.

    Args:
        image: The image to draw on.
        winner: The winner of the round.
    """
    if winner != 'tie':
        text = f'{winner.upper()} WINS!'
        font_scale = 2
        font = cv2.FONT_HERSHEY_TRIPLEX
        
        # Calculate the text size to center it
        (text_width, text_height), baseline = cv2.getTextSize(
            text, 
            font, 
            font_scale, 
            2
        )
        center_x = (image.shape[1] - text_width) // 2
        center_y = (image.shape[0] + text_height) // 2

        # Draw the text with a shadow
        cv2.putText(
            image,
            text,
            (center_x, center_y),
            font,
            font_scale,
            (0, 0, 0),
            5,
            cv2.LINE_AA,
        )

        # Draw the main text
        cv2.putText(
            image,
            text,
            (center_x, center_y),
            font,
            font_scale,
            (0, 255, 0) if winner == 'player' else (0, 0, 255),
            2,
            cv2.LINE_AA,
        )
        
        cv2.imshow('Rock, Paper, Scissors', image)
        cv2.waitKey(1000)
