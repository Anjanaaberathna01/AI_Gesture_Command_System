import pyautogui


class ScrollController:

    def __init__(
        self,
        scroll_threshold=0.008,
        scroll_amount=30
    ):

        self.scroll_threshold = scroll_threshold
        self.scroll_amount = scroll_amount

        self.previous_y = None
        self.accumulated_movement = 0

        print("Scroll Controller initialized!")

    def scroll(self, current_y):

        if self.previous_y is None:

            self.previous_y = current_y
            return

        movement = self.previous_y - current_y

        self.previous_y = current_y

        self.accumulated_movement += movement

        if abs(self.accumulated_movement) >= self.scroll_threshold:

            if self.accumulated_movement > 0:

                self.scroll_up()

            else:

                self.scroll_down()

            self.accumulated_movement = 0

    def scroll_up(self):

        pyautogui.scroll(self.scroll_amount)

        print("SCROLL UP")

    def scroll_down(self):

        pyautogui.scroll(-self.scroll_amount)

        print("SCROLL DOWN")

    def reset(self):

        self.previous_y = None
        self.accumulated_movement = 0