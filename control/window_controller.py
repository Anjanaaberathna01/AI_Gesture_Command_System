import ctypes
import time

from ctypes import wintypes


class WindowController:

    SW_MINIMIZE = 6
    SW_MAXIMIZE = 3

    GW_HWNDNEXT = 2

    def __init__(self, cooldown=1.0):

        self.cooldown = cooldown
        self.last_action_time = 0
        self.target_window = None

        self.user32 = ctypes.WinDLL("user32", use_last_error=True)

        # Correct Windows API types
        self.user32.GetForegroundWindow.restype = wintypes.HWND

        self.user32.GetWindow.argtypes = [
            wintypes.HWND,
            wintypes.UINT
        ]
        self.user32.GetWindow.restype = wintypes.HWND

        self.user32.GetWindowTextLengthW.argtypes = [
            wintypes.HWND
        ]
        self.user32.GetWindowTextLengthW.restype = ctypes.c_int

        self.user32.GetWindowTextW.argtypes = [
            wintypes.HWND,
            wintypes.LPWSTR,
            ctypes.c_int
        ]

        self.user32.IsWindow.argtypes = [wintypes.HWND]
        self.user32.IsWindow.restype = wintypes.BOOL

        self.user32.IsWindowVisible.argtypes = [wintypes.HWND]
        self.user32.IsWindowVisible.restype = wintypes.BOOL

        self.user32.ShowWindow.argtypes = [
            wintypes.HWND,
            ctypes.c_int
        ]
        self.user32.ShowWindow.restype = wintypes.BOOL

        self.user32.SetForegroundWindow.argtypes = [wintypes.HWND]
        self.user32.SetForegroundWindow.restype = wintypes.BOOL

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

        if not hwnd:
            return None

        title = self._get_window_title(hwnd)

        # If OpenCV window is foreground, find another visible window
        if "AI Gesture Command System" in title:

            hwnd = self.user32.GetWindow(
                hwnd,
                self.GW_HWNDNEXT
            )

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

    def capture_target_window(self):

        hwnd = self._get_target_window()

        if not hwnd:
            print("No target window found")
            return False

        self.target_window = hwnd

        print(
            "Target window selected:",
            self._get_window_title(hwnd)
        )

        return True

    def maximize_target_window(self):

        if not self.target_window:
            print("No target window selected")
            return False

        if not self.user32.IsWindow(self.target_window):
            self.target_window = None
            print("Target window is no longer available")
            return False

        current_time = time.time()

        if current_time - self.last_action_time < self.cooldown:
            return False

        self.user32.ShowWindow(
            self.target_window,
            self.SW_MAXIMIZE
        )

        self.user32.SetForegroundWindow(
            self.target_window
        )

        self.last_action_time = current_time

        print("Target window maximized")

        return True

    def minimize_target_window(self):

        if not self.target_window:
            print("No target window selected")
            return False

        if not self.user32.IsWindow(self.target_window):
            self.target_window = None
            print("Target window is no longer available")
            return False

        current_time = time.time()

        if current_time - self.last_action_time < self.cooldown:
            return False

        self.user32.ShowWindow(
            self.target_window,
            self.SW_MINIMIZE
        )

        self.last_action_time = current_time

        print("Target window minimized")

        return True