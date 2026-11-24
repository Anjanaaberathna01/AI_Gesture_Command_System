
import time


class SwipeCommandController:

    def __init__(self, cooldown=1.0):
        self.cooldown = cooldown
        self.last_command_time = 0

    def can_execute(self):

        current_time = time.time()

        if current_time - self.last_command_time >= self.cooldown:

            self.last_command_time = current_time
            return True

        return False
