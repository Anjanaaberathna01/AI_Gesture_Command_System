
import math


class ThumbBendDetector:

    def __init__(self, bend_threshold=145):

        self.bend_threshold = bend_threshold

        print("Thumb Bend Detector initialized!")

    def calculate_angle(self, a, b, c):

        ba_x = a.x - b.x
        ba_y = a.y - b.y

        bc_x = c.x - b.x
        bc_y = c.y - b.y

        dot = ba_x * bc_x + ba_y * bc_y

        mag_a = math.sqrt(ba_x**2 + ba_y**2)
        mag_c = math.sqrt(bc_x**2 + bc_y**2)

        if mag_a == 0 or mag_c == 0:
            return 0.0

        cosine = dot / (mag_a * mag_c)
        cosine = max(-1.0, min(1.0, cosine))

        return math.degrees(math.acos(cosine))

    def detect_bend(self, hand_landmarks):

        # Thumb landmarks
        mcp = hand_landmarks[2]
        ip = hand_landmarks[3]
        tip = hand_landmarks[4]

        angle = self.calculate_angle(
            mcp,
            ip,
            tip
        )

        is_bent = angle < self.bend_threshold

        return {
            "Angle": round(angle, 2),
            "Bent": is_bent,
            "State": "BENT" if is_bent else "EXTENDED"
        }
