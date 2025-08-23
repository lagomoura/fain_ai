def get_hand_gesture(hand_landmarks):
    """
    Determine the hand gesture (rock, paper, or scissors) from hand landmarks.

    Args:
        hand_landmarks: A list of hand landmarks detected by MediaPipe.

    Returns:
        The detected gesture as a string ('rock', 'paper', 'scissors', or 'unknown').
    """
    # Get the coordinates of the fingertips and the base of the fingers
    thumb_tip = hand_landmarks.landmark[4]
    index_tip = hand_landmarks.landmark[8]
    middle_tip = hand_landmarks.landmark[12]
    ring_tip = hand_landmarks.landmark[16]
    pinky_tip = hand_landmarks.landmark[20]

    thumb_ip = hand_landmarks.landmark[3]
    index_pip = hand_landmarks.landmark[6]
    middle_pip = hand_landmarks.landmark[10]
    ring_pip = hand_landmarks.landmark[14]
    pinky_pip = hand_landmarks.landmark[18]

    # Check for paper (all fingers extended)
    if (index_tip.y < index_pip.y and
            middle_tip.y < middle_pip.y and
            ring_tip.y < ring_pip.y and
            pinky_tip.y < pinky_pip.y and
            thumb_tip.x < thumb_ip.x):
        return 'paper'

    # Check for scissors (index and middle fingers extended)
    if (index_tip.y < index_pip.y and
            middle_tip.y < middle_pip.y and
            ring_tip.y > ring_pip.y and
            pinky_tip.y > pinky_pip.y):
        return 'scissors'

    # Check for rock (all fingers curled)
    if (index_tip.y > index_pip.y and
            middle_tip.y > middle_pip.y and
            ring_tip.y > ring_pip.y and
            pinky_tip.y > pinky_pip.y and
            thumb_tip.x > thumb_ip.x):
        return 'rock'

    return 'unknown'
