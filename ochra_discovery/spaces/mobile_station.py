from ochra_common.spaces.mobile_station import MobileStation
from ochra_common.utils.mixins import RestProxyMixinReadOnly
from uuid import UUID


class MobileStation(MobileStation, RestProxyMixinReadOnly):
    def __init__(self, object_id: UUID):
        """Station object that provides access to the devices and robots.

        Args:
            object_id (UUID): UUID of Station
        """
        super().__init__()
        self._mixin_hook(self._endpoint, object_id)

    def get_mobile_robot(self):
        return self._lab_conn.get_object("robots", self.mobile_robot)
