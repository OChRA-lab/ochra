from .abstract import IkaPlateAbstract
from ochra.common.utils.mixins import RestProxyMixinReadOnly


class IkaPlate(IkaPlateAbstract, RestProxyMixinReadOnly):
    def __init__(self, name):
        super().__init__()
        self._mixin_hook(self._endpoint, name)

    def set_temperature(self, temperature: int) -> bool:
        return self._lab_conn.call_on_object(
            self._endpoint, self.id, "set_temperature", {"temperature": temperature}
        )

    def start_heat(self) -> bool:
        return self._lab_conn.call_on_object(self._endpoint, self.id, "start_heat", {})

    def stop_heat(self) -> bool:
        return self._lab_conn.call_on_object(self._endpoint, self.id, "stop_heat", {})

    def set_speed(self, speed: int) -> bool:
        return self._lab_conn.call_on_object(
            self._endpoint, self.id, "set_speed", {"speed": speed}
        )

    def start_stir(self) -> bool:
        return self._lab_conn.call_on_object(self._endpoint, self.id, "start_stir", {})

    def stop_stir(self) -> bool:
        return self._lab_conn.call_on_object(self._endpoint, self.id, "stop_stir", {})
