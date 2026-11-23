import time


class SwipeDetector:

    def __init__(
        self,
        swipe_threshold=0.15,
        max_swipe_time=0.5,
        cooldown=0.5
    ):

        self.swipe_threshold = swipe_threshold
        self.max_swipe_time = max_swipe_time
        self.cooldown = cooldown

        self.start_position = None
        self.start_time = None

        self.last_swipe_time = 0

    def detect_swipe(self, current_x):

        current_time = time.time()

        # Cooldown check
        if current_time - self.last_swipe_time < self.cooldown:
            return None

        # Initialize starting position
        if self.start_position is None:

            self.start_position = current_x
            self.start_time = current_time

            return None

        # Calculate movement
        movement = current_x - self.start_position

        elapsed_time = current_time - self.start_time

        # Check maximum swipe duration
        if elapsed_time > self.max_swipe_time:

            self.start_position = current_x
            self.start_time = current_time

            return None

        # Detect right swipe
        if movement >= self.swipe_threshold:

            self.last_swipe_time = current_time

            self.reset()

            return "SWIPE_RIGHT"

        # Detect left swipe
        elif movement <= -self.swipe_threshold:

            self.last_swipe_time = current_time

            self.reset()

            return "SWIPE_LEFT"

        return None

    def reset(self):

        self.start_position = None
        self.start_time = None