
class FingerDetector:

    def __init__(self):

        print("Finger Detector initialized!")

    def detect_fingers(self, hand_landmarks, handedness):

        fingers = {}

        # =========================
        # THUMB DETECTION
        # =========================

        import math


        thumb_tip = hand_landmarks[4]
        thumb_ip = hand_landmarks[3]
        thumb_mcp = hand_landmarks[2]
        index_mcp = hand_landmarks[5]

        def distance(p1, p2):

            return math.sqrt(
                (p1.x - p2.x) ** 2 +
                (p1.y - p2.y) ** 2
            )

        tip_to_index = distance(thumb_tip, index_mcp)
        mcp_to_index = distance(thumb_mcp, index_mcp)

        fingers["Thumb"] = (
            tip_to_index > mcp_to_index * 1.25
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
