
import cv2
import time

from camera.webcam import Webcam
from vision.hand_tracker import HandTracker
from gestures.finger_detector import FingerDetector
from gestures.gesture_recognizer import GestureRecognizer
from control.mouse_controller import MouseController
from control.mouse_controller import MouseClickController
from gestures.thumb_bend_detector import ThumbBendDetector


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

    finger_detector = FingerDetector()
    gesture_recognizer = GestureRecognizer()
    mouse_click_controller = MouseClickController(
        debounce_time=0.08,
        double_click_interval=0.35,
        execute_clicks=False
    )
    thumb_bend_detector = ThumbBendDetector(
        bend_threshold=165
    )
    mouse_controller = MouseController(
        smoothing=0.25
    )
    previous_gestures = {}

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
            # Detect hand landmarks
            frame = tracker.draw_landmarks(
                frame,
                result
            )

            hand_count = len(result.hand_landmarks)

            # =========================
            # FINGER DETECTION
            # =========================

            if hand_count > 0:

                for hand_index, hand_landmarks in enumerate(
                    result.hand_landmarks
                ):

                    handedness = result.handedness[
                        hand_index
                    ][0].category_name

                    fingers = finger_detector.detect_fingers(
                        hand_landmarks,
                        handedness
                    )

                    # Recognize gesture
                    gesture = gesture_recognizer.recognize(fingers)

                    # Thumb Bend Detection
                    thumb_data = thumb_bend_detector.detect_bend(
                        hand_landmarks
                    )

                    print(
                        f"{handedness} Hand | "
                        f"Thumb Angle: {thumb_data['Angle']} | "
                        f"Thumb State: {thumb_data['State']}"
                    )
                    # Mouse Click Control
                    mouse_click_controller.update(
                        thumb_data['State'] == "BENT"
                    )

                    # Mouse Cursor Control
                    if gesture == "POINTING":

                        index_tip = hand_landmarks[8]

                        mouse_controller.move_cursor(
                            index_tip.x,
                            index_tip.y
                        )

                    # Print only when gesture changes
                    if previous_gestures.get(hand_index) != gesture:

                        print(
                            f"{handedness} Hand | "
                            f"Gesture: {gesture} | "
                            f"Fingers: {fingers['Count']}"
                        )

                        previous_gestures[hand_index] = gesture

                    # Display gesture on webcam
                    height, width, _ = frame.shape

                    wrist = hand_landmarks[0]

                    text_x = int(wrist.x * width)
                    text_y = int(wrist.y * height) - 20

                    cv2.putText(
                        frame,
                        gesture,
                        (text_x, max(text_y, 150)),
                        cv2.FONT_HERSHEY_SIMPLEX,
                        0.8,
                        (0, 255, 255),
                        2
                    )

                    print(
                        handedness,
                        "Hand:",
                        fingers
                    )

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
        mouse_controller.release()
        tracker.close()
        webcam.release()


if __name__ == "__main__":
    main()
