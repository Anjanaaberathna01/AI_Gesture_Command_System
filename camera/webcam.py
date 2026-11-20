import cv2  # type: ignore[reportMissingImports]
import time


class Webcam:
    def __init__(self, camera_index=0, width=640, height=480):
        self.camera_index = camera_index
        # Initialize webcam
        self.cap = cv2.VideoCapture(
            camera_index,
            cv2.CAP_DSHOW
        )
        if not self.cap.isOpened():
            raise RuntimeError(
                f"Cannot open camera: {camera_index}"
            )
        # Set camera resolution
        self.cap.set(
            cv2.CAP_PROP_FRAME_WIDTH,
            width
        )
        self.cap.set(
            cv2.CAP_PROP_FRAME_HEIGHT,
            height
        )
        # Reduce camera buffer delay
        self.cap.set(
            cv2.CAP_PROP_BUFFERSIZE,
            1
        )
        self.width = width
        self.height = height

        print("Webcam initialized successfully!")
        print(f"Camera Index: {camera_index}")
        print(f"Resolution: {width}x{height}")

    def read_frame(self):
        success, frame = self.cap.read()
        if not success:
            return None
        # Mirror the webcam image
        frame = cv2.flip(frame, 1)
        return frame

    def release(self):
        if self.cap is not None:
            self.cap.release()
        cv2.destroyAllWindows()

        print("Webcam released successfully!")