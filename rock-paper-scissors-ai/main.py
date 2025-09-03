import cv2
import mediapipe as mp
import time
import argparse
from src.game import get_computer_choice, get_winner
from src.hand_gesture import get_hand_gesture
from src.ui import display_ui
from src.animations import display_winner_animation
from src.assets import load_images
from src.sounds import load_sounds, play_sound

# Initialize MediaPipe Hands
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(
    static_image_mode=False,
    max_num_hands=1,
    min_detection_confidence=0.7,
    min_tracking_confidence=0.5,
)
mp_drawing = mp.solutions.drawing_utils

# Load images and sounds
images = load_images()
sounds = load_sounds()

# ---------------------------------------------------------------------------
# CLI arguments
# ---------------------------------------------------------------------------


parser = argparse.ArgumentParser(description='Rock-Paper-Scissors AI')
parser.add_argument(
    '--difficulty',
    '-d',
    default='normal',
    help='AI difficulty: easy | medium | hard (default: normal = medium)',
)
args = parser.parse_args()

# Map "normal" → "medium" for the underlying AI while keeping the label the
# user passed for display purposes.
difficulty_cli = args.difficulty.lower()
game_difficulty = 'medium' if difficulty_cli == 'normal' else difficulty_cli

# Use the USB webcam on index 1 by default. Adjust as required for your
# system (e.g., 0 for built-in or virtual cameras).
cap = cv2.VideoCapture(1)

# Game state
scores = {'player': 0, 'computer': 0}
player_choice = 'unknown'
computer_choice = 'unknown'
winner = 'unknown'
last_gesture_time = time.time()
round_start_time = time.time()
show_countdown = True
countdown_sound_played = {3: False, 2: False, 1: False}

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    # Flip the frame horizontally for a later selfie-view display
    # and convert the BGR image to RGB.
    image = cv2.cvtColor(cv2.flip(frame, 1), cv2.COLOR_BGR2RGB)

    # To improve performance, optionally mark the image as not writeable to
    # pass by reference.
    image.flags.writeable = False
    results = hands.process(image)

    # Draw the hand annotations on the image.
    image.flags.writeable = True
    image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

    # Countdown timer
    if show_countdown:
        elapsed_time = time.time() - round_start_time
        countdown = 3 - int(elapsed_time)
        if countdown > 0:
            cv2.putText(
                image,
                str(countdown),
                (
                    image.shape[1] // 2 - 50,
                    image.shape[0] // 2 + 50,
                ),
                cv2.FONT_HERSHEY_TRIPLEX,
                4,
                (255, 255, 255),
                5,
            )
            if not countdown_sound_played[countdown]:
                play_sound(sounds.get('countdown'))
                countdown_sound_played[countdown] = True
        else:
            show_countdown = False
            last_gesture_time = time.time()
            countdown_sound_played = {3: False, 2: False, 1: False} # Reset for next round

    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            mp_drawing.draw_landmarks(
                image,
                hand_landmarks,
                mp_hands.HAND_CONNECTIONS,
            )

            # Recognize the gesture after the countdown
            if (not show_countdown and 
                    time.time() - last_gesture_time > 1):
                player_choice = get_hand_gesture(hand_landmarks)

                if player_choice != 'unknown':
                    computer_choice = get_computer_choice(difficulty=game_difficulty)
                    winner = get_winner(player_choice, computer_choice)

                    if winner == 'player':
                        scores['player'] += 1
                        play_sound(sounds.get('win'))
                    elif winner == 'computer':
                        scores['computer'] += 1
                        play_sound(sounds.get('lose'))
                    
                    display_winner_animation(image, winner)
                    
                    # Reset for the next round
                    round_start_time = time.time()
                    show_countdown = True

                last_gesture_time = time.time()

    # Display the UI
    display_ui(
        image,
        player_choice,
        computer_choice,
        winner,
        scores,
        images,
        difficulty=difficulty_cli,
    )

    # Show the image
    cv2.imshow('Rock, Paper, Scissors', image)

    # Break the loop when 'ESC' is pressed
    if cv2.waitKey(5) & 0xFF == 27:
        break

cap.release()
cv2.destroyAllWindows()
