from ochra_common.spaces.work_station import WorkStation
from ochra_common.utils.mixins import RestProxyMixinReadOnly
from uuid import UUID

class WorkStation(WorkStation, RestProxyMixinReadOnly):
    def __init__(self, object_id: UUID):
        super().__init__()
        self._mixin_hook(self._endpoint, object_id)