from ochra.common.equipment.operation import Operation
from ochra.common.utils.mixins import RestProxyMixinReadOnly

from .abstract import FumeHoodSash


class FumeHoodSash(FumeHoodSash, RestProxyMixinReadOnly):
    """Workflow-side proxy for the Opta-backed fume hood sash."""

    def __init__(self, name: str):
        super().__init__()
        self._mixin_hook(self._endpoint, name)

    def connect_device(self) -> Operation:
        return self._lab_conn.call_on_object(self._endpoint, self.id, "connect_device", {})

    def disconnect_device(self) -> Operation:
        return self._lab_conn.call_on_object(self._endpoint, self.id, "disconnect_device", {})

    def is_connected(self) -> Operation:
        return self._lab_conn.call_on_object(self._endpoint, self.id, "is_connected", {})

    def is_idle(self) -> Operation:
        return self._lab_conn.call_on_object(self._endpoint, self.id, "is_idle", {})

    def move_up(self) -> Operation:
        return self._lab_conn.call_on_object(self._endpoint, self.id, "move_up", {})

    def move_down(self) -> Operation:
        return self._lab_conn.call_on_object(self._endpoint, self.id, "move_down", {})

    def verification_details(self) -> Operation:
        return self._lab_conn.call_on_object(self._endpoint, self.id, "verification_details", {})

    def verify_binding(self) -> Operation:
        return self._lab_conn.call_on_object(self._endpoint, self.id, "verify_binding", {})

    def status_snapshot(self) -> Operation:
        return self._lab_conn.call_on_object(self._endpoint, self.id, "status_snapshot", {})
