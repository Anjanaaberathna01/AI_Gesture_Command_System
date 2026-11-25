
import ctypes
import time


class WindowController:

    SW_MINIMIZE = 6
    SW_RESTORE = 9
    GW_HWNDNEXT = 2

    def __init__(self, cooldown=1.0):

        self.cooldown = cooldown
        self.last_action_time = 0
        self.target_window = None

        self.user32 = ctypes.windll.user32

    def _get_window_title(self, hwnd):

        length = self.user32.GetWindowTextLengthW(hwnd)

        buffer = ctypes.create_unicode_buffer(length + 1)

        self.user32.GetWindowTextW(
            hwnd,
            buffer,
            length + 1
        )

        return buffer.value

    def _get_target_window(self):

        hwnd = self.user32.GetForegroundWindow()

        title = self._get_window_title(hwnd)

        # Skip our own OpenCV camera window
        if "AI Gesture Command System" in title:

            hwnd = self.user32.GetWindow(hwnd, self.GW_HWNDNEXT)

            while hwnd:

                title = self._get_window_title(hwnd)

                if (
                    self.user32.IsWindowVisible(hwnd)
                    and title
                    and "AI Gesture Command System" not in title
                ):
                    return hwnd

                hwnd = self.user32.GetWindow(
                    hwnd,
                    self.GW_HWNDNEXT
                )

            return None

        return hwnd

    def minimize_window(self):

        current_time = time.time()

        if current_time - self.last_action_time < self.cooldown:
            return False

        hwnd = self._get_target_window()

        if not hwnd:
            return False

        self.target_window = hwnd

        self.user32.ShowWindow(
            hwnd,
            self.SW_MINIMIZE
        )

        self.last_action_time = current_time

        print("Window Minimized")

        return True

    def restore_window(self):

        current_time = time.time()

        if current_time - self.last_action_time < self.cooldown:
            return False

        if not self.target_window:
            print("No minimized window available to restore")
            return False

        if not self.user32.IsWindow(self.target_window):
            self.target_window = None
            return False

        self.user32.ShowWindow(
            self.target_window,
            self.SW_RESTORE
        )

        self.user32.SetForegroundWindow(
            self.target_window
        )

        self.last_action_time = current_time

        print("Window Restored")

        return True
