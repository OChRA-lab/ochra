from ochra_common.spaces.location import Location
from ochra_common.equipment.device import Device
from ochra_common.spaces.work_station import WorkStation
from ochra_common.utils.mixins import RestProxyMixin
from typing import List, Type
from uuid import UUID
from pydantic import Field
from ..storage.inventory import Inventory


class WorkStation(WorkStation, RestProxyMixin):
    devices: List[UUID] = Field(default_factory=list)
    port: int = Field(default=None)

    def __init__(self, name: str, location: Location):
        super().__init__(
            collection="stations",
            name=name,
            location=location,
            module_path="ochra_discovery.spaces.work_station",
        )
        self.inventory = Inventory(
            owner=self.get_base_model(), containers_max_capacity=100
        )
        self._mixin_hook("stations", self.id)

    def add_device(self, device: Type[Device]):
        device.owner_station = self.get_base_model()
        devices = self.devices
        devices.append(device.id)
        self.devices = devices
