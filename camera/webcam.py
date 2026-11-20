
import cv2


class Webcam:

    def __init__(
        self,
        camera_index=0,
        width=640,
        height=480
    ):

        self.cap = cv2.VideoCapture(
            camera_index,
            cv2.CAP_MSMF
        )

        if not self.cap.isOpened():
            raise RuntimeError("Camera could not open!")

        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, width)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, height)

        print("Camera opened successfully!")
        print("Camera Index:", camera_index)
        print(
            "Resolution:",
            int(self.cap.get(cv2.CAP_PROP_FRAME_WIDTH)),
            "x",
            int(self.cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        )

    def read_frame(self):

        success, frame = self.cap.read()

        if not success:
            print("Frame capture failed!")
            return None

        return frame

    def release(self):

        if self.cap.isOpened():
            self.cap.release()

        cv2.destroyAllWindows()

        print("Webcam released successfully!")
