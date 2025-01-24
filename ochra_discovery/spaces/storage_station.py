from ochra_common.spaces.storage_station import StorageStation
from ochra_common.utils.mixins import RestProxyMixinReadOnly
from uuid import UUID


class StorageStation(StorageStation, RestProxyMixinReadOnly):
    def __init__(self, object_id: UUID):
        """Station object that provides access to the devices and robots.

        Args:
            object_id (UUID): UUID of Station
        """
        super().__init__()
        self._mixin_hook(self._endpoint, object_id)
