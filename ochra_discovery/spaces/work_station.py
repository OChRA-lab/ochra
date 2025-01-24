from ochra_common.equipment.device import Device
from ochra_common.equipment.robot import Robot
from ochra_common.spaces.work_station import WorkStation
from ochra_common.utils.mixins import RestProxyMixinReadOnly
from uuid import UUID
from typing import Type, Union


class WorkStation(WorkStation, RestProxyMixinReadOnly):
    def __init__(self, object_id: UUID):
        """Station object that provides access to the devices and robots.

        Args:
            object_id (UUID): UUID of Station
        """
        super().__init__()
        self._mixin_hook(self._endpoint, object_id)

    def get_device(self, device_identifier: Union[str, UUID]) -> Type[Device]:
        """Get a device object by name or UUID.

        Args:
            device_identifier (Union[str, UUID]): Name or UUID of the device to get.

        Returns:
            Type[Device]: The device object.
        """
        return self._lab_conn.get_object("devices", device_identifier)

    def get_robot(self, robot_identifier: Union[str, UUID]) -> Type[Robot]:
        """Get a robot object by name or UUID.

        Args:
            robot_identifier (Union[str, UUID]): Name or UUID of the robot to get.

        Returns:
            Type[Robot]: The robot object.
        """
        return self._lab_conn.get_object("robots", robot_identifier)
