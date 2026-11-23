from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume


class VolumeController:

    def __init__(self, volume_step=0.05):

        self.volume_step = volume_step

        devices = AudioUtilities.GetSpeakers()

        interface = devices.Activate(
            IAudioEndpointVolume._iid_,
            CLSCTX_ALL,
            None
        )

        self.volume_control = cast(
            interface,
            POINTER(IAudioEndpointVolume)
        )

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

        print(
            f"Volume: {volume * 100:.0f}%"
        )

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