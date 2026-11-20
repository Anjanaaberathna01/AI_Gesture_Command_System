import cv2 #type: ignore
import time

from camera.webcam import Webcam


def main():

    # Initialize webcam
    webcam = Webcam(
        camera_index=0,
        width=640,
        height=480
    )

    previous_time = time.time()

    try:

        while True:

            # Read webcam frame
            frame = webcam.read_frame()

            if frame is None:
                print("Failed to capture frame!")
                break

            # Calculate FPS
            current_time = time.time()

            fps = 1 / (current_time - previous_time)

            previous_time = current_time

            # Display FPS
            cv2.putText(
                frame,
                f"FPS: {int(fps)}",
                (20, 40),
                cv2.FONT_HERSHEY_SIMPLEX,
                1,
                (0, 255, 0),
                2
            )

            # Display status
            cv2.putText(
                frame,
                "CAMERA ACTIVE",
                (20, 80),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.7,
                (0, 255, 0),
                2
            )

            # Display video
            cv2.imshow(
                "AI Gesture Command System - Webcam",
                frame
            )

            # Exit using Q or ESC
            key = cv2.waitKey(1) & 0xFF

            if key == ord('q') or key == 27:
                break

    finally:

        webcam.release()


if __name__ == "__main__":
    main()