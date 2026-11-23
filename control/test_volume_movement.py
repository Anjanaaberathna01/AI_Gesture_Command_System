
from volume_controller import VolumeController


controller = VolumeController(
    volume_step=0.05
)

print("\nInitial Volume:")
print(f"{controller.get_volume() * 100:.0f}%")

# Simulate hand moving UP
print("\nMoving UP...")

controller.adjust_volume(0.60)
controller.adjust_volume(0.59)
controller.adjust_volume(0.58)
controller.adjust_volume(0.57)
controller.adjust_volume(0.56)

# Simulate hand moving DOWN
print("\nMoving DOWN...")

controller.reset_movement()

controller.adjust_volume(0.40)
controller.adjust_volume(0.41)
controller.adjust_volume(0.42)
controller.adjust_volume(0.43)
controller.adjust_volume(0.44)

print("\nFinal Volume:")
print(f"{controller.get_volume() * 100:.0f}%")

controller.release()
