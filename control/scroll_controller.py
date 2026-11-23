
import pyautogui


class ScrollController:

    def __init__(self, scroll_threshold=0.015, scroll_amount=20):

        self.scroll_threshold = scroll_threshold
        self.scroll_amount = scroll_amount

        self.previous_y = None

        print("Scroll Controller initialized!")

    def scroll(self, current_y):

        if self.previous_y is None:
            self.previous_y = current_y
            return

        movement = self.previous_y - current_y

        if abs(movement) >= self.scroll_threshold:

            if movement > 0:
                self.scroll_up()

            else:
                self.scroll_down()

            self.previous_y = current_y

    def scroll_up(self):

        pyautogui.scroll(self.scroll_amount)

        print("SCROLL UP")

    def scroll_down(self):

        pyautogui.scroll(-self.scroll_amount)

        print("SCROLL DOWN")

    def reset(self):

        self.previous_y = None
