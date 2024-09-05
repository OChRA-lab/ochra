from .abstract import IkaPlateAbstract
from ochra_common.utils.mixins import RestProxyMixin


class IkaPlate(IkaPlateAbstract, RestProxyMixin):
    def __init__(self, name, station_id):
        super().__init__(name=name, station_id=station_id)
        self._mixin_hook("devices", self.id)
        self._lab_init("devices")

    def set_temperature(self, temperature: int) -> bool:
        self.temperature = temperature
        return True

    def start_heat(self) -> bool:
        print("do the thing")
        return True

    def stop_heat(self) -> bool:
        print("do the thing")
        return True

    def set_speed(self, speed: int) -> bool:
        print("do the thing")
        return True

    def start_stir(self) -> bool:
        print("do the thing")
        return True

    def stop_stir(self) -> bool:
        print("do the thing")
        return True

    @staticmethod
    def from_name(self, name: str):
        pass
