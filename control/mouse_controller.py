
import pyautogui


class MouseController:

    def __init__(self, smoothing=0.25):

        self.screen_width, self.screen_height = pyautogui.size()

        self.smoothing = smoothing

        self.current_x = self.screen_width // 2
        self.current_y = self.screen_height // 2

        pyautogui.FAILSAFE = True
        pyautogui.PAUSE = 0

        print("Mouse Controller initialized!")
        print(
            f"Screen: {self.screen_width}x{self.screen_height}"
        )

    def move_cursor(self, landmark_x, landmark_y):

        target_x = int(landmark_x * self.screen_width)
        target_y = int(landmark_y * self.screen_height)

        # Keep cursor within screen boundaries
        target_x = max(
            0,
            min(target_x, self.screen_width - 1)
        )

        target_y = max(
            0,
            min(target_y, self.screen_height - 1)
        )

        # Smooth cursor movement
        self.current_x += (
            target_x - self.current_x
        ) * self.smoothing

        self.current_y += (
            target_y - self.current_y
        ) * self.smoothing

        pyautogui.moveTo(
            int(self.current_x),
            int(self.current_y)
        )

    def release(self):

        print("Mouse Controller released!")
