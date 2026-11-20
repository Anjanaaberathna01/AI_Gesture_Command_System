
class FingerDetector:

    def __init__(self):

        print("Finger Detector initialized!")

    def detect_fingers(self, hand_landmarks, handedness):

        fingers = {}

        # =========================
        # THUMB
        # =========================

        thumb_tip = hand_landmarks[4]
        thumb_ip = hand_landmarks[3]

        if handedness == "Right":

            fingers["Thumb"] = (
                thumb_tip.x < thumb_ip.x
            )

        else:

            fingers["Thumb"] = (
                thumb_tip.x > thumb_ip.x
            )

        # =========================
        # INDEX FINGER
        # =========================

        fingers["Index"] = (
            hand_landmarks[8].y <
            hand_landmarks[6].y
        )

        # =========================
        # MIDDLE FINGER
        # =========================

        fingers["Middle"] = (
            hand_landmarks[12].y <
            hand_landmarks[10].y
        )

        # =========================
        # RING FINGER
        # =========================

        fingers["Ring"] = (
            hand_landmarks[16].y <
            hand_landmarks[14].y
        )

        # =========================
        # PINKY FINGER
        # =========================

        fingers["Pinky"] = (
            hand_landmarks[20].y <
            hand_landmarks[18].y
        )

        # Count open fingers

        fingers["Count"] = sum(
            fingers[finger]
            for finger in [
                "Thumb",
                "Index",
                "Middle",
                "Ring",
                "Pinky"
            ]
        )

        return fingers
