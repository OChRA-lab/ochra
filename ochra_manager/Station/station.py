from .communicator import Communicator
from ochra_common.spaces.work_station import WorkStation
from ochra_common.utils.mixins import RestProxyMixin


class Station(Communicator, WorkStation, RestProxyMixin):
    def __init__(self, name, location, offline=False):
        super().__init__(name=name, location=location)
        self._offline = offline

    def add_device(self, device):
        devices = self._devices
        devices.append(device)
        self._devices = devices
