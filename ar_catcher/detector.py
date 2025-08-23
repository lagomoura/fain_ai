import cv2
import mediapipe as mp


class HandTracker:
    """Wrapper around MediaPipe Hands that exposes landmark positions in pixel coordinates."""

    INDEX_TIP_ID = 8  # landmark id for index fingertip

    def __init__(
        self,
        max_num_hands: int = 2,
        detection_confidence: float = 0.7,
        tracking_confidence: float = 0.6,
    ) -> None:
        self._mp_hands = mp.solutions.hands
        self._hands = self._mp_hands.Hands(
            max_num_hands=max_num_hands,
            min_detection_confidence=detection_confidence,
            min_tracking_confidence=tracking_confidence,
        )
        self._mp_drawing = mp.solutions.drawing_utils

    def process(self, frame_bgr):
        frame_rgb = cv2.cvtColor(frame_bgr, cv2.COLOR_BGR2RGB)
        return self._hands.process(frame_rgb)

    def draw(self, frame_bgr, results):
        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                self._mp_drawing.draw_landmarks(
                    frame_bgr,
                    hand_landmarks,
                    self._mp_hands.HAND_CONNECTIONS,
                )

    @staticmethod
    def landmarks_to_pixels(landmarks, frame_width: int, frame_height: int):
        """Convert normalized landmarks to pixel (x, y) list."""
        pixels = []
        for lm in landmarks.landmark:
            px, py = int(lm.x * frame_width), int(lm.y * frame_height)
            pixels.append((px, py))
        return pixels



