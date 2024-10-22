from ochra_common.equipment.device import Device
from ochra_common.spaces.work_station import WorkStation
from ochra_common.utils.mixins import RestProxyMixinReadOnly
from uuid import UUID
from typing import Type, Union

class WorkStation(WorkStation, RestProxyMixinReadOnly):
    def __init__(self, object_id: UUID):
        super().__init__()
        self._mixin_hook(self._endpoint, object_id)

    def get_device(self, device_identifier: Union[str, UUID]) -> Type[Device]:
        return self._lab_conn.get_object("devices", device_identifier)