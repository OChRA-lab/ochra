from ochra_common.spaces.location import Location
from ochra_common.equipment.device import Device
from ochra_common.spaces.station import Station
from ochra_common.utils.mixins import RestProxyMixin
from ochra_common.utils.enum import StationType
from typing import List, Type
from uuid import UUID
from pydantic import Field
from ..storage.inventory import Inventory


class Station(Station, RestProxyMixin):
    devices: List[UUID] = Field(default_factory=list)
    port: int = Field(default=None)

    def __init__(self, name: str, type: StationType, location: Location, port: int):
        super().__init__(
            collection="stations",
            name=name,
            type=type,
            location=location,
            module_path="ochra_discovery.spaces.station",
            locked=None
        )
        self.port = port
        self.inventory = Inventory(
            owner=self.get_base_model(), containers_max_capacity=100
        )
        self._mixin_hook("stations", self.id)

    def add_device(self, device: Type[Device]):
        device.owner_station = self.id
        devices = self.devices
        devices.append(device.id)
        self.devices = devices
