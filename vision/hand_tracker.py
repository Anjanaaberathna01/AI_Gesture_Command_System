import cv2
import mediapipe as mp

from mediapipe.tasks import python
from mediapipe.tasks.python import vision


class HandTracker:

    def __init__(
        self,
        model_path="models/hand_landmarker.task",
        max_hands=2,
        detection_confidence=0.5,
        tracking_confidence=0.5
    ):

        # Model configuration
        base_options = python.BaseOptions(
            model_asset_path=model_path
        )

        options = vision.HandLandmarkerOptions(
            base_options=base_options,
            running_mode=vision.RunningMode.VIDEO,
            num_hands=max_hands,
            min_hand_detection_confidence=detection_confidence,
            min_hand_presence_confidence=0.5,
            min_tracking_confidence=tracking_confidence
        )

        # Initialize AI model
        self.landmarker = vision.HandLandmarker.create_from_options(
            options
        )

        self.mp_connections = vision.HandLandmarker.HAND_CONNECTIONS

        print("MediaPipe Hand Tracker initialized!")

    def detect_hands(self, frame, timestamp_ms):

        # Convert BGR to RGB
        rgb_frame = cv2.cvtColor(
            frame,
            cv2.COLOR_BGR2RGB
        )

        # Convert to MediaPipe image
        mp_image = mp.Image(
            image_format=mp.ImageFormat.SRGB,
            data=rgb_frame
        )

        # Run hand detection
        result = self.landmarker.detect_for_video(
            mp_image,
            timestamp_ms
        )

        return result

    def draw_landmarks(self, frame, result):

        if not result.hand_landmarks:
            return frame

        height, width, _ = frame.shape

        # Draw each detected hand
        for hand_landmarks in result.hand_landmarks:

            # Draw connections
            for connection in self.mp_connections:

                start = hand_landmarks[connection.start]
                end = hand_landmarks[connection.end]

                start_point = (
                    int(start.x * width),
                    int(start.y * height)
                )

                end_point = (
                    int(end.x * width),
                    int(end.y * height)
                )

                cv2.line(
                    frame,
                    start_point,
                    end_point,
                    (0, 255, 0),
                    2
                )

            # Draw 21 landmarks
            for landmark in hand_landmarks:

                x = int(landmark.x * width)
                y = int(landmark.y * height)

                cv2.circle(
                    frame,
                    (x, y),
                    5,
                    (0, 0, 255),
                    -1
                )

        return frame

    def close(self):

        self.landmarker.close()

        print("Hand Tracker closed!")