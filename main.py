
import cv2
import time

from camera.webcam import Webcam
from vision.hand_tracker import HandTracker


def main():

    webcam = Webcam(
        camera_index=0,
        width=640,
        height=480
    )

    tracker = HandTracker(
        model_path="models/hand_landmarker.task",
        max_hands=2,
        detection_confidence=0.5,
        tracking_confidence=0.5
    )

    previous_time = time.time()
    frame_counter = 0

    try:

        while True:

            frame = webcam.read_frame()

            if frame is None:
                print("Camera frame error!")
                break

            timestamp_ms = int(time.perf_counter() * 1000)

            # Detect hands
            result = tracker.detect_hands(
                frame,
                timestamp_ms
            )

            # Draw hand landmarks
            frame = tracker.draw_landmarks(
                frame,
                result
            )

            # Count detected hands
            hand_count = len(result.hand_landmarks)

            frame_counter += 1

            if frame_counter % 30 == 0:
                print("Detected hands:", hand_count)

            # Calculate FPS
            current_time = time.time()
            fps = 1 / max(current_time - previous_time, 0.001)
            previous_time = current_time

            cv2.putText(
                frame,
                f"FPS: {int(fps)}",
                (20, 40),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.8,
                (0, 255, 0),
                2
            )

            cv2.putText(
                frame,
                f"Hands Detected: {hand_count}",
                (20, 80),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.8,
                (255, 0, 0),
                2
            )

            if hand_count > 0:
                status = "HAND TRACKING ACTIVE"
                color = (0, 255, 0)
            else:
                status = "NO HAND DETECTED"
                color = (0, 0, 255)

            cv2.putText(
                frame,
                status,
                (20, 120),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.7,
                color,
                2
            )

            cv2.imshow(
                "AI Gesture Command System",
                frame
            )

            key = cv2.waitKey(1) & 0xFF

            if key == ord("q") or key == 27:
                break

    finally:

        tracker.close()
        webcam.release()


if __name__ == "__main__":
    main()
