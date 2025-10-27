from ochra_common.spaces.location import Location
from ochra_common.equipment.device import Device
from ochra_common.equipment.operation import Operation
from ochra_common.spaces.station import Station
from ochra_common.utils.mixins import RestProxyMixin
from ochra_common.utils.enum import StationType, PatchType
from typing import List, Type
from uuid import UUID
from pydantic import Field
from ..storage.inventory import Inventory


class Station(Station, RestProxyMixin):
    """
    Represents a laboratory station containing devices, robots, and inventory.
    """

    devices: List[UUID] = Field(default_factory=list)
    """List of device IDs associated with the station."""

    port: int = Field(default=None)
    """Network port number for the station."""

    def __init__(self, name: str, type: StationType, location: Location, port: int):
        super().__init__(
            collection="stations",
            name=name,
            type=type,
            location=location,
            module_path="ochra_discovery.spaces.station",
            locked=None,
        )
        self.port = port

        self._mixin_hook("stations", self.id)
        if self.inventory is None or self.inventory == []:
            
            inventory = Inventory(
                owner=self.get_base_model(), containers_max_capacity=100
            )
            self.inventory = inventory.get_base_model()

    def add_device(self, device: Type[Device]) -> None:
        """
        Add a device to the station's list of devices
        
        Args:
            device (Type[Device]): The device to add to the station
        """
        device.owner_station = self.id
        self._lab_conn.patch_property(self._endpoint, self.id, "devices", device.id, PatchType.LIST_APPEND)

    def add_operation(self, op: Operation) -> None:
        """
        Add an operation to the station's list of operations

        Args:
            op (Operation): The operation to add to the station
        """
        self._lab_conn.patch_property(self._endpoint, self.id, "operation_record", op, PatchType.LIST_APPEND)
