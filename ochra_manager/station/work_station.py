from ochra_common.spaces.location import Location
from ochra_common.equipment.device import Device
from ochra_common.spaces.work_station import WorkStation
from ochra_common.utils.mixins import RestProxyMixin
from typing import List, Type
from uuid import UUID
from pydantic import Field


class WorkStation(WorkStation, RestProxyMixin):
    devices: List[UUID] = Field(default_factory=list)

    def __init__(self, name: str, location: Location):
        super().__init__(name=name, location=location, module_path="ochra_discovery.spaces.work_station")
        self._mixin_hook("stations", self.id)

    def add_device(self, device: Type[Device]):
        devices = self.devices
        devices.append(device.id)
        self.devices = devices
