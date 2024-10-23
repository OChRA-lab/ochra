from .abstract import IkaPlateAbstract
from ochra_common.utils.mixins import RestProxyMixinReadOnly
from ochra_common.connections.lab_connection import LabConnection


class IkaPlate(IkaPlateAbstract, RestProxyMixinReadOnly):
    _endpoint = "devices"

    def __init__(self, name):
        self._mixin_hook("devices", name)

    def set_temperature(self, temperature: int) -> bool:
        lab_conn = LabConnection()
        return lab_conn.call_on_object("devices", self.id, "set_temperature", {"temperature": temperature})

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
