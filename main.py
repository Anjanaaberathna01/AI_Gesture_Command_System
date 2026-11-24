
import cv2
import time

from camera.webcam import Webcam
from vision.hand_tracker import HandTracker

from gestures.finger_detector import FingerDetector
from gestures.gesture_recognizer import GestureRecognizer
from gestures.thumb_bend_detector import ThumbBendDetector
from gestures.swipe_detector import SwipeDetector

from control.mouse_controller import MouseController
from control.mouse_click_controller import MouseClickController
from control.scroll_controller import ScrollController
from control.volume_controller import VolumeController


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
        double_click_interval=0.45,
        execute_clicks=False
    )

    thumb_bend_detector = ThumbBendDetector(
        bend_threshold=160
    )

    mouse_controller = MouseController(
        smoothing=0.25
    )

    scroll_controller = ScrollController(
        scroll_threshold=0.008,
        scroll_amount=30
    )

    volume_controller = VolumeController(
        volume_step=0.05
    )

    # Swipe detectors (one for each hand)
    swipe_detectors = {}

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

            # =========================
            # HAND DETECTION
            # =========================

            result = tracker.detect_hands(
                frame,
                timestamp_ms
            )

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

                    gesture = gesture_recognizer.recognize(
                        fingers
                    )

                    # =========================
                    # SWIPE DETECTOR INITIALIZATION
                    # =========================

                    if hand_index not in swipe_detectors:

                        swipe_detectors[hand_index] = SwipeDetector(
                            swipe_threshold=0.11,
                            max_swipe_time=0.8,
                            cooldown=0.6
                        )

                    # =========================
                    # THUMB BEND DETECTION
                    # =========================

                    thumb_data = thumb_bend_detector.detect_bend(
                        hand_landmarks
                    )

                    is_thumb_bent = thumb_data["Bent"]

                    mouse_click_controller.update(
                        is_thumb_bent
                    )

                    # =========================
                    # GESTURE CONTROLS
                    # =========================

                    swipe = None

                    if gesture == "THREE_FINGER":

                        # Volume Control
                        wrist = hand_landmarks[0]

                        volume_controller.adjust_volume(
                            wrist.y
                        )

                        scroll_controller.reset()

                        swipe_detectors[hand_index].reset()

                    elif gesture == "POINTING":

                        # Mouse Movement
                        volume_controller.reset_movement()

                        index_tip = hand_landmarks[8]

                        mouse_controller.move_cursor(
                            index_tip.x,
                            index_tip.y
                        )

                        scroll_controller.reset()

                        swipe_detectors[hand_index].reset()

                    elif gesture == "PEACE":

                        # Scroll Control
                        volume_controller.reset_movement()

                        index_tip = hand_landmarks[8]

                        scroll_controller.scroll(
                            index_tip.y
                        )

                        swipe_detectors[hand_index].reset()

                    elif gesture == "OPEN_PALM":
                        # swipe detection for open palm gesture   
                        swipe = swipe_detectors[
                            hand_index].detect_swipe(wrist.x)
                        if swipe:
                            print(f"Right Hand | Detected Gesture: {swipe}")


                    else:
                        # Reset all controls when no specific gesture is detected
                        swipe_detectors[hand_index].reset()    
                        # Stop other movement controls
                        volume_controller.reset_movement()

                        scroll_controller.reset()

                        # =========================
                        # SWIPE DETECTION
                        # =========================

                        wrist = hand_landmarks[0]

                        print(
                            f"Gesture: {gesture} | "
                            f"Wrist X: {wrist.x:.3f}"
                        )

                        swipe = swipe_detectors[
                            hand_index
                        ].detect_swipe(wrist.x)

                        print(f"Swipe Result: {swipe}")

                        if swipe is not None:

                            print(
                                f"{handedness} Hand | "
                                f"Detected Gesture: {swipe}"
                            )

                    # =========================
                    # GESTURE CHANGE DETECTION
                    # =========================

                    if previous_gestures.get(hand_index) != gesture:

                        print(
                            f"{handedness} Hand | "
                            f"Gesture: {gesture} | "
                            f"Fingers: {fingers['Count']}"
                        )

                    previous_gestures[hand_index] = gesture

                    # =========================
                    # DISPLAY ON WEBCAM
                    # =========================

                    height, width, _ = frame.shape

                    wrist = hand_landmarks[0]

                    text_x = int(wrist.x * width)
                    text_y = int(wrist.y * height) - 20

                    display_text = swipe if swipe else gesture

                    cv2.putText(
                        frame,
                        display_text,
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

            # =========================
            # FRAME COUNTER
            # =========================

            frame_counter += 1

            if frame_counter % 30 == 0:

                print(
                    "Detected hands:",
                    hand_count
                )

            # =========================
            # FPS CALCULATION
            # =========================

            current_time = time.time()

            fps = 1 / max(
                current_time - previous_time,
                0.001
            )

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

                # Reset swipe tracking when no hands are detected
                for detector in swipe_detectors.values():
                    detector.reset()

                volume_controller.reset_movement()
                scroll_controller.reset()

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
        volume_controller.release()
        tracker.close()
        webcam.release()

        cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
