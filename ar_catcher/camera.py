import cv2


class Camera:
    """Simple OpenCV camera wrapper with context manager support."""

    def __init__(self, src: int = 0):
        self.src = src
        self.cap = None

    def __enter__(self):
        self.cap = cv2.VideoCapture(self.src)
        if not self.cap.isOpened():
            raise RuntimeError("Could not open camera source")
        return self

    def __exit__(self, exc_type, exc, tb):
        if self.cap is not None:
            self.cap.release()
        cv2.destroyAllWindows()

    def read(self):
        if self.cap is None:
            raise RuntimeError("Camera not initialized")
        ret, frame = self.cap.read()
        if not ret:
            raise RuntimeError("Failed to read frame from camera")
        return frame



