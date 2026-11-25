# AI Gesture Command System 🖐️

A real-time, AI-powered gesture recognition system that allows users to control their computer through hand gestures using a webcam.

The system uses computer vision and hand landmark detection to recognize gestures and perform computer operations such as mouse movement, scrolling, volume adjustment, browser navigation, and window management.

## 🚀 Features

- **Real-Time Hand Tracking** – Detects and tracks hand landmarks using a webcam.
- **Finger Detection** – Identifies individual finger positions and states.
- **Gesture Recognition** – Recognizes predefined hand gestures.
- **Mouse Movement** – Controls the mouse cursor using the index finger.
- **Mouse Click Detection** – Detects thumb-bend gestures for mouse click interactions.
- **Scrolling** – Scrolls content using the Peace gesture.
- **Volume Control** – Adjusts system volume using a three-finger gesture.
- **Swipe Detection** – Detects left and right hand movements.
- **Browser Navigation** – Navigates backward and forward using swipe gestures.
- **Window Management** – Controls application windows using a gesture sequence.
- **Real-Time Status Display** – Displays detected gestures, commands, hand count, and FPS.

## 🖐️ Gesture Controls

| Hand Gesture               | Action                         |
| -------------------------- | ------------------------------ |
| ☝️ Pointing                | Move mouse cursor              |
| ✌️ Peace                   | Scroll up and down             |
| 🤟 Three Fingers           | Adjust system volume           |
| 🖐️ Open Palm              | Activate swipe detection       |
| 👊 Fist → Open Palm        | Maximize selected window       |
| 👊 Fist → Open Palm → Fist | Minimize selected window       |
| Thumb Bend                 | Detect mouse click interaction |

## 🛠️ Technologies Used

- Python
- OpenCV
- MediaPipe
- PyAutoGUI
- NumPy
- ctypes
- Computer Vision
- Hand Landmark Detection

## 📁 Project Structure

```text
AI_Gesture_Command_System/
│
├── camera/
│   └── webcam.py
│
├── vision/
│   └── hand_tracker.py
│
├── gestures/
│   ├── finger_detector.py
│   ├── gesture_recognizer.py
│   ├── thumb_bend_detector.py
│   └── swipe_detector.py
│
├── control/
│   ├── mouse_controller.py
│   ├── mouse_click_controller.py
│   ├── scroll_controller.py
│   ├── volume_controller.py
│   ├── browser_controller.py
│   ├── swipe_command_controller.py
│   └── window_controller.py
│
├── models/
│   └── hand_landmarker.task
│
├── main.py
├── requirements.txt
└── README.md
```

## ⚙️ Installation

### 1. Clone the Repository

```bash
git clone https://github.com/Anjanaaberathna01/AI_Gesture_Command_System.git
```

### 2. Navigate to the Project Directory

```bash
cd AI_Gesture_Command_System
```

### 3. Create a Virtual Environment

```bash
python -m venv venv
```

### 4. Activate the Virtual Environment

**Windows:**

```bash
venv\Scripts\activate
```

### 5. Install Dependencies

```bash
pip install -r requirements.txt
```

### 6. Download the Hand Landmarker Model

Download the MediaPipe Hand Landmarker model and place it inside the `models/` directory.

Model path:

```text
models/hand_landmarker.task
```

### 7. Run the Application

```bash
python main.py
```

## 🎮 How to Use

1. Connect a webcam to your computer.
2. Run the application using `python main.py`.
3. Allow the system to detect your hand.
4. Place your hand within the webcam's field of view.
5. Perform the supported gestures to control your computer.
6. Press **Q** or **ESC** to exit the application.

## 📊 Real-Time Monitoring

The application displays:

- Current recognized gesture
- Detected swipe direction
- Last executed command
- Frames per second (FPS)
- Number of detected hands
- Hand tracking status

## 🔮 Future Improvements

- Improve gesture recognition accuracy.
- Add more customizable hand gestures.
- Improve mouse click and double-click interactions.
- Add gesture calibration and sensitivity settings.
- Develop a graphical user interface (GUI).
- Optimize performance and reduce detection latency.
- Support additional computer control operations.

## 👨‍💻 Author

**Anjana Aberathna**

Computer Science Undergraduate | AI & Software Development Enthusiast

## 📄 License

This project is developed for educational and research purposes. A license can be added when the project is prepared for public distribution.
