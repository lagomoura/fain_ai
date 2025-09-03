import cv2
import os  # Added for environment variable support


class Camera:
    """Simple OpenCV camera wrapper with context manager support."""

    def __init__(self, src: int | None = None, auto_scan_range: int = 5):
        """Create a camera wrapper.

        Precedence for selecting a camera source:
        1. Environment variable ``AR_CAM_INDEX`` (must be an int)
        2. The ``src`` argument explicitly provided by the caller
        3. Automatic scan from 0 to ``auto_scan_range``-1 and pick the first
           index that provides a valid frame.
        """

        env_src = os.getenv('AR_CAM_INDEX')
        if env_src is not None and env_src.isdigit():
            self.src = int(env_src)
        elif src is not None:
            self.src = src
        else:
            self.src = self._auto_detect(auto_scan_range)

        self.cap = None

    # ---------------------------------------------------------------------
    # Private helpers
    # ---------------------------------------------------------------------

    def _auto_detect(self, max_indices: int) -> int:
        """Return the first camera index that yields frames.

        Iterates over indices ``0..max_indices-1`` and returns the first one
        that opens successfully *and* provides a frame. Raises a
        ``RuntimeError`` if none of the indices work.
        """
        for idx in range(max_indices):
            cap = cv2.VideoCapture(idx)
            if cap.isOpened():
                ret, frame = cap.read()
                if ret and frame is not None:
                    cap.release()
                    return idx
            cap.release()

        raise RuntimeError(
            f'No working camera found in indices 0-{max_indices - 1}.'
        )

    def __enter__(self):
        print(f'📷 Connecting to camera index {self.src}...')
        self.cap = cv2.VideoCapture(self.src)
        
        if not self.cap.isOpened():
            raise RuntimeError(f"Could not open camera source: {self.src}")
        
        # Test if we can actually read frames
        ret, test_frame = self.cap.read()
        if ret and test_frame is not None:
            print('✅ Camera stream established successfully')
            print(f'📷 Using camera index {self.src}')
        else:
            raise RuntimeError("Camera opened but no frames received")
        
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



