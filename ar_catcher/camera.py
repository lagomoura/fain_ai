import cv2


class Camera:
    """Simple OpenCV camera wrapper with context manager support."""

    def __init__(self, src=None):
        # Use camera index 0 by default (DroidCam registered as system camera)
        if src is None:
            self.src = 0  # Direct connection to system camera index 0
        else:
            self.src = src
        self.cap = None

    def __enter__(self):
        print("📱 Connecting to DroidCam through system camera index 0...")
        self.cap = cv2.VideoCapture(self.src)
        
        if not self.cap.isOpened():
            raise RuntimeError(f"Could not open camera source: {self.src}")
        
        # Test if we can actually read frames
        ret, test_frame = self.cap.read()
        if ret and test_frame is not None:
            print("✅ SUCCESS! DroidCam is working through system camera")
            print(f"📱 Using: camera index {self.src} (DroidCam system camera)")
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



