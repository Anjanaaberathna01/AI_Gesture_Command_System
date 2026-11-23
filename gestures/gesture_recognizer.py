
class GestureRecognizer:

    def __init__(self):
        print("Gesture Recognizer initialized!")

    def recognize(self, fingers):

        thumb = fingers["Thumb"]
        index = fingers["Index"]
        middle = fingers["Middle"]
        ring = fingers["Ring"]
        pinky = fingers["Pinky"]

        # Open Palm
        if all([thumb, index, middle, ring, pinky]):
            return "OPEN_PALM"

        # Closed Fist
        if not any([thumb, index, middle, ring, pinky]):
            return "FIST"

        # Pointing
        if (
            index and
            not any([thumb, middle, ring, pinky])
        ):
            return "POINTING"

        # Peace Sign
        if (
            index and middle and
            not any([thumb, ring, pinky])
        ):
            return "PEACE"

        # Three Finger Gesture
        if (
            index and middle and ring and
            not thumb and not pinky
        ):
            return "THREE_FINGER"

        return "UNKNOWN"
