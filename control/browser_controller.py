import pyautogui


class BrowserController:

    def swipe_left(self):
        pyautogui.hotkey("alt", "left")
        print("Browser: BACK")

    def swipe_right(self):
        pyautogui.hotkey("alt", "right")
        print("Browser: FORWARD")