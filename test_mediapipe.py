from pathlib import Path
import mediapipe as mp

from mediapipe.tasks import python
from mediapipe.tasks.python import vision


print("1. MediaPipe imported successfully!")

model_path = Path("models/hand_landmarker.task")

print("2. Model exists:", model_path.exists())

if not model_path.exists():
    raise FileNotFoundError("Hand landmark model not found!")

base_options = python.BaseOptions(
    model_asset_path=str(model_path)
)

options = vision.HandLandmarkerOptions(
    base_options=base_options,
    running_mode=vision.RunningMode.VIDEO,
    num_hands=2,
    min_hand_detection_confidence=0.5,
    min_hand_presence_confidence=0.5,
    min_tracking_confidence=0.5
)

print("3. Loading MediaPipe model...")

tracker = vision.HandLandmarker.create_from_options(
    options
)

print("4. SUCCESS! MediaPipe Hand Tracker initialized!")

tracker.close()

print("5. Model closed successfully!")