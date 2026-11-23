from pycaw.pycaw import AudioUtilities


class VolumeController:

    def __init__(self, volume_step=0.05):

        self.volume_step = volume_step
        self.previous_y = None
        self.accumulated_movement = 0
        self.movement_threshold = 0.025

        device = AudioUtilities.GetSpeakers()

        if device is None:
            raise RuntimeError("No audio output device found!")

        self.volume_control = device.EndpointVolume

        print("Volume Controller initialized!")

        print(
            f"Current Volume: "
            f"{self.get_volume() * 100:.0f}%"
        )

    def get_volume(self):

        return self.volume_control.GetMasterVolumeLevelScalar()

    def set_volume(self, volume):

        volume = max(0.0, min(volume, 1.0))

        self.volume_control.SetMasterVolumeLevelScalar(
            volume,
            None
        )

        print(f"Volume: {volume * 100:.0f}%")

    def increase_volume(self):

        current_volume = self.get_volume()

        new_volume = current_volume + self.volume_step

        self.set_volume(new_volume)

    def decrease_volume(self):

        current_volume = self.get_volume()

        new_volume = current_volume - self.volume_step

        self.set_volume(new_volume)

    def release(self):

        print("Volume Controller released!")

    def adjust_volume(self, current_y):

        if self.previous_y is None:

            self.previous_y = current_y
            return

        movement = self.previous_y - current_y
        self.previous_y = current_y
        self.accumulated_movement += movement

        if self.accumulated_movement >= self.movement_threshold:
            self.increase_volume()
            self.accumulated_movement = 0

        elif self.accumulated_movement <= -self.movement_threshold:
            self.decrease_volume()
            self.accumulated_movement = 0
    
    def reset_movement(self):
        """
        Reset the accumulated movement.
        """
        self.previous_y = None
        self.accumulated_movement = 0