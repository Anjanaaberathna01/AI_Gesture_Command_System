
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
from control.browser_controller import BrowserController
from control.swipe_command_controller import SwipeCommandController


def main():

    # =========================
    # WEBCAM INITIALIZATION
    # =========================

    webcam = Webcam(
        camera_index=0,
        width=640,
        height=480
    )

    # =========================
    # HAND TRACKER INITIALIZATION
    # =========================

    tracker = HandTracker(
        model_path="models/hand_landmarker.task",
        max_hands=2,
        detection_confidence=0.5,
        tracking_confidence=0.5
    )

    # =========================
    # DETECTOR INITIALIZATION
    # =========================

    finger_detector = FingerDetector()
    gesture_recognizer = GestureRecognizer()

    thumb_bend_detector = ThumbBendDetector(
        bend_threshold=160
    )

    # =========================
    # CONTROLLER INITIALIZATION
    # =========================

    mouse_controller = MouseController(
        smoothing=0.25
    )

    mouse_click_controller = MouseClickController(
        debounce_time=0.08,
        double_click_interval=0.45,
        execute_clicks=False
    )

    scroll_controller = ScrollController(
        scroll_threshold=0.008,
        scroll_amount=30
    )

    volume_controller = VolumeController(
        volume_step=0.05
    )

    browser_controller = BrowserController()

    swipe_command_controller = SwipeCommandController(
        cooldown=1.0
    )

    # =========================
    # SWIPE DETECTORS
    # =========================

    swipe_detectors = {}

    # =========================
    # GESTURE TRACKING
    # =========================

    previous_gestures = {}

    # =========================
    # DISPLAY VARIABLES
    # =========================

    last_command = "NONE"
    current_swipe = "NONE"
    current_gesture = "NO HAND"

    # =========================
    # FPS VARIABLES
    # =========================

    previous_time = time.time()
    frame_counter = 0

    try:

        # =========================
        # MAIN LOOP
        # =========================

        while True:

            frame = webcam.read_frame()

            if frame is None:

                print("Camera frame error!")
                break

            # Reset per-frame display values
            current_swipe = "NONE"
            current_gesture = "NO HAND"

            timestamp_ms = int(
                time.perf_counter() * 1000
            )

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

            hand_count = len(
                result.hand_landmarks
            )

            # =========================
            # FINGER DETECTION
            # =========================

            if hand_count > 0:

                for hand_index, hand_landmarks in enumerate(
                    result.hand_landmarks
                ):

                    # Get handedness
                    handedness = result.handedness[
                        hand_index
                    ][0].category_name

                    # Detect fingers
                    fingers = finger_detector.detect_fingers(
                        hand_landmarks,
                        handedness
                    )

                    # Recognize gesture
                    gesture = gesture_recognizer.recognize(
                        fingers
                    )

                    current_gesture = gesture

                    # Get wrist landmark
                    wrist = hand_landmarks[0]

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

                    # -------------------------
                    # THREE FINGER - VOLUME
                    # -------------------------

                    if gesture == "THREE_FINGER":

                        volume_controller.adjust_volume(
                            wrist.y
                        )

                        scroll_controller.reset()

                        swipe_detectors[hand_index].reset()

                        current_swipe = "NONE"

                    # -------------------------
                    # POINTING - MOUSE MOVEMENT
                    # -------------------------

                    elif gesture == "POINTING":

                        volume_controller.reset_movement()

                        index_tip = hand_landmarks[8]

                        mouse_controller.move_cursor(
                            index_tip.x,
                            index_tip.y
                        )

                        scroll_controller.reset()

                        swipe_detectors[hand_index].reset()

                        current_swipe = "NONE"

                    # -------------------------
                    # PEACE - SCROLL
                    # -------------------------

                    elif gesture == "PEACE":

                        volume_controller.reset_movement()

                        index_tip = hand_landmarks[8]

                        scroll_controller.scroll(
                            index_tip.y
                        )

                        swipe_detectors[hand_index].reset()

                        current_swipe = "NONE"

                    # -------------------------
                    # OPEN PALM - SWIPE
                    # -------------------------

                    elif gesture == "OPEN_PALM":

                        # Stop other movement controls
                        volume_controller.reset_movement()
                        scroll_controller.reset()

                        # Detect swipe using wrist X
                        swipe = swipe_detectors[
                            hand_index
                        ].detect_swipe(wrist.x)

                        if swipe is not None:

                            current_swipe = swipe

                            # Check command cooldown
                            if swipe_command_controller.can_execute():

                                if swipe == "SWIPE_LEFT":

                                    browser_controller.swipe_left()

                                    last_command = "BROWSER BACK"

                                    print(
                                        "Browser Back Executed"
                                    )

                                elif swipe == "SWIPE_RIGHT":

                                    browser_controller.swipe_right()

                                    last_command = "BROWSER FORWARD"

                                    print(
                                        "Browser Forward Executed"
                                    )

                            else:

                                print(
                                    "Swipe command blocked by cooldown"
                                )

                    # -------------------------
                    # UNKNOWN / OTHER GESTURES
                    # -------------------------

                    else:

                        swipe_detectors[hand_index].reset()

                        volume_controller.reset_movement()

                        scroll_controller.reset()

                        current_swipe = "NONE"

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
                    # DISPLAY GESTURE NEAR HAND
                    # =========================

                    height, width, _ = frame.shape

                    text_x = int(wrist.x * width)
                    text_y = int(wrist.y * height) - 20

                    display_text = (
                        swipe if swipe else gesture
                    )

                    cv2.putText(
                        frame,
                        display_text,
                        (text_x, max(text_y, 150)),
                        cv2.FONT_HERSHEY_SIMPLEX,
                        0.8,
                        (0, 255, 255),
                        2
                    )

                    # =========================
                    # DEBUG OUTPUT
                    # =========================

                    print(
                        handedness,
                        "Hand:",
                        fingers
                    )

            else:

                # =========================
                # NO HAND DETECTED
                # =========================

                for detector in swipe_detectors.values():

                    detector.reset()

                volume_controller.reset_movement()

                scroll_controller.reset()

                current_swipe = "NONE"
                current_gesture = "NO HAND"

                previous_gestures.clear()

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

            # =========================
            # SYSTEM STATUS
            # =========================

            if hand_count > 0:

                status = "HAND TRACKING ACTIVE"
                status_color = (0, 255, 0)

            else:

                status = "NO HAND DETECTED"
                status_color = (0, 0, 255)

            # =========================
            # SYSTEM DISPLAY
            # =========================

            cv2.putText(
                frame,
                "AI GESTURE COMMAND SYSTEM",
                (20, 30),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.7,
                (0, 255, 0),
                2
            )

            cv2.putText(
                frame,
                f"Gesture: {current_gesture}",
                (20, 70),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.6,
                (255, 255, 255),
                2
            )

            cv2.putText(
                frame,
                f"Swipe: {current_swipe}",
                (20, 110),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.6,
                (0, 255, 255),
                2
            )

            cv2.putText(
                frame,
                f"Last Command: {last_command}",
                (20, 150),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.6,
                (255, 255, 255),
                2
            )

            cv2.putText(
                frame,
                f"FPS: {int(fps)}",
                (20, 190),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.6,
                (0, 255, 0),
                2
            )

            cv2.putText(
                frame,
                f"Hands Detected: {hand_count}",
                (20, 230),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.6,
                (255, 0, 0),
                2
            )

            cv2.putText(
                frame,
                status,
                (20, 270),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.6,
                status_color,
                2
            )

            # =========================
            # SHOW WEBCAM
            # =========================

            cv2.imshow(
                "AI Gesture Command System",
                frame
            )

            # =========================
            # KEYBOARD CONTROL
            # =========================

            key = cv2.waitKey(1) & 0xFF

            if key == ord("q") or key == 27:

                break

    finally:

        # =========================
        # RELEASE RESOURCES
        # =========================

        mouse_controller.release()

        volume_controller.release()

        tracker.close()

        webcam.release()

        cv2.destroyAllWindows()


# =========================
# PROGRAM ENTRY POINT
# =========================

if __name__ == "__main__":

    main()
