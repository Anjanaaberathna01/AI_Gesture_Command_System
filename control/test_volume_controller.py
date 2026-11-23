from volume_controller import VolumeController

import time


volume_controller = VolumeController(
    volume_step=0.05
)

print("\nTesting Volume Increase...")

volume_controller.increase_volume()

time.sleep(1)

print("\nTesting Volume Decrease...")

volume_controller.decrease_volume()

time.sleep(1)

print("\nTesting Volume Set...")

volume_controller.set_volume(0.50)

time.sleep(1)

print("\nFinal Volume:")

print(
    f"{volume_controller.get_volume() * 100:.0f}%"
)

volume_controller.release()