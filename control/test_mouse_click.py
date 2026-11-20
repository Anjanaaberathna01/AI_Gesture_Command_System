
import time

from control.mouse_click_controller import MouseClickController


controller = MouseClickController(
    debounce_time=0.08,
    double_click_interval=0.35,
    execute_clicks=False
)


def set_state(is_bent, duration=0.15):

    controller.update(is_bent)
    time.sleep(duration)
    controller.update(is_bent)


# Initial thumb extended
set_state(False, 0.15)

# Single click: bend -> extend
set_state(True, 0.15)
set_state(False, 0.15)

time.sleep(0.5)
controller.update(False)

# Double click: bend -> extend -> bend -> extend
set_state(True, 0.15)
set_state(False, 0.15)
set_state(True, 0.15)
set_state(False, 0.15)

time.sleep(0.5)
controller.update(False)

print("Click Controller Test Completed!")
