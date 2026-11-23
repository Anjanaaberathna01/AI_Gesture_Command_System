import time

from gestures.swipe_detector import SwipeDetector


def main():

    detector = SwipeDetector(
        swipe_threshold=0.15,
        max_swipe_time=0.5,
        cooldown=0.5
    )

    test_positions = [
        0.70,
        0.65,
        0.60,
        0.50,
        0.45
    ]

    print("Testing Right Swipe...")

    for position in test_positions:

        result = detector.detect_swipe(position)

        print(
            f"X: {position:.2f} | "
            f"Gesture: {result}"
        )

        time.sleep(0.05)


if __name__ == "__main__":
    main()