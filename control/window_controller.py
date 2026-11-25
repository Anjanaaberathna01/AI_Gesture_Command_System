
import pyautogui
import time


class WindowController:

    def __init__(self, cooldown=1.0):

        self.cooldown = cooldown
        self.last_action_time = 0

    def minimize_window(self):

        current_time = time.time()

        if current_time - self.last_action_time < self.cooldown:
            return False

        pyautogui.hotkey("win", "down")

        self.last_action_time = current_time

        print("Window Minimized")

        return True

    def restore_window(self):

        current_time = time.time()

        if current_time - self.last_action_time < self.cooldown:
            return False

        pyautogui.hotkey("win", "up")

        self.last_action_time = current_time

        print("Window Restored")

        return True
