
import time
import pyautogui


class MouseClickController:

    def __init__(
        self,
        debounce_time=0.08,
        double_click_interval=0.35,
        execute_clicks=False
    ):

        self.debounce_time = debounce_time
        self.double_click_interval = double_click_interval
        self.execute_clicks = execute_clicks

        self.raw_state = None
        self.raw_state_time = time.monotonic()

        self.stable_state = None

        self.pending_click_time = None

        print("Mouse Click Controller initialized!")
        print("Click execution:", execute_clicks)

    def update(self, is_bent):

        current_time = time.monotonic()

        # Detect raw thumb state changes
        if is_bent != self.raw_state:

            self.raw_state = is_bent
            self.raw_state_time = current_time

        # Confirm state after debounce period
        if (
            current_time - self.raw_state_time
            >= self.debounce_time
        ):

            if self.stable_state != self.raw_state:

                previous_state = self.stable_state
                self.stable_state = self.raw_state

                # Thumb changed from BENT to EXTENDED
                if previous_state is True and self.stable_state is False:

                    self.register_click(current_time)

        # Check whether pending single click should execute
        if self.pending_click_time is not None:

            elapsed = current_time - self.pending_click_time

            if elapsed > self.double_click_interval:

                self.single_click()
                self.pending_click_time = None

    def register_click(self, current_time):

        if self.pending_click_time is None:

            self.pending_click_time = current_time

        else:

            elapsed = current_time - self.pending_click_time

            if elapsed <= self.double_click_interval:

                self.double_click()
                self.pending_click_time = None

            else:

                self.single_click()
                self.pending_click_time = current_time

    def single_click(self):

        print("SINGLE CLICK DETECTED")

        if self.execute_clicks:
            pyautogui.click(button="left")

    def double_click(self):

        print("DOUBLE CLICK DETECTED")

        if self.execute_clicks:
            pyautogui.doubleClick(
                interval=0.1,
                button="left"
            )
