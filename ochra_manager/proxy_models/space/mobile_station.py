from ochra_common.spaces.location import Location
from ochra_common.equipment.mobile_robot import MobileRobot
from ochra_common.spaces.mobile_station import MobileStation
from ochra_common.utils.mixins import RestProxyMixin
from typing import Type
from uuid import UUID
from pydantic import Field
from ..storage.inventory import Inventory


class MobileStation(MobileStation, RestProxyMixin):
    robot: UUID = Field(default=None)
    port: int = Field(default=None)

    def __init__(self, name: str, location: Location, port: int):
        super().__init__(
            collection="stations",
            name=name,
            location=location,
            module_path="ochra_discovery.spaces.mobile_station",
        )
        self.port = port
        self.inventory = Inventory(
            owner=self.get_base_model(), containers_max_capacity=100
        )
        self._mixin_hook("stations", self.id)

    def add_mobile_robot(self, mobile_robot: Type[MobileRobot]):
        mobile_robot.owner_station = self.id
        self.mobile_robot = mobile_robot.id
