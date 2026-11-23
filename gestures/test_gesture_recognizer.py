
from gesture_recognizer import GestureRecognizer


recognizer = GestureRecognizer()


test_cases = [
    {
        "name": "OPEN_PALM",
        "fingers": {
            "Thumb": True,
            "Index": True,
            "Middle": True,
            "Ring": True,
            "Pinky": True
        }
    },
    {
        "name": "FIST",
        "fingers": {
            "Thumb": False,
            "Index": False,
            "Middle": False,
            "Ring": False,
            "Pinky": False
        }
    },
    {
        "name": "POINTING",
        "fingers": {
            "Thumb": False,
            "Index": True,
            "Middle": False,
            "Ring": False,
            "Pinky": False
        }
    },
    {
        "name": "PEACE",
        "fingers": {
            "Thumb": False,
            "Index": True,
            "Middle": True,
            "Ring": False,
            "Pinky": False
        }
    },
    {
        "name": "THREE_FINGER",
        "fingers": {
            "Thumb": False,
            "Index": True,
            "Middle": True,
            "Ring": True,
            "Pinky": False
        }
    }
]


for test in test_cases:

    result = recognizer.recognize(test["fingers"])

    expected = test["name"]

    status = "PASS" if result == expected else "FAIL"

    print(
        f"{test['name']} | "
        f"Detected: {result} | "
        f"{status}"
    )


print("\nGesture Recognition Test Completed!")
