
import time
from collections import deque


class SwipeDetector:

    def __init__(
        self,
        swipe_threshold=0.11,
        max_swipe_time=0.8,
        cooldown=0.6
    ):

        self.swipe_threshold = swipe_threshold
        self.max_swipe_time = max_swipe_time
        self.cooldown = cooldown

        self.positions = deque()

        self.last_swipe_time = 0

    def detect_swipe(self, current_x):

        current_time = time.time()

        # Cooldown check
        if current_time - self.last_swipe_time < self.cooldown:
            return None

        # Add current position
        self.positions.append(
            (current_time, current_x)
        )

        # Remove old positions
        while self.positions:

            elapsed = current_time - self.positions[0][0]

            if elapsed > self.max_swipe_time:
                self.positions.popleft()

            else:
                break

        # Need at least two positions
        if len(self.positions) < 2:
            return None

        start_x = self.positions[0][1]

        movement = current_x - start_x

        # Right swipe
        if movement >= self.swipe_threshold:

            self.last_swipe_time = current_time
            self.reset()

            return "SWIPE_RIGHT"

        # Left swipe
        elif movement <= -self.swipe_threshold:

            self.last_swipe_time = current_time
            self.reset()

            return "SWIPE_LEFT"

        return None

    def reset(self):

        self.positions.clear()
