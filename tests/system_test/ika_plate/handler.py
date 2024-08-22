from .abstract import IkaPlateAbstract
from ochra_common.utils.db_decorator import backend_db


@backend_db
class IkaPlate(IkaPlateAbstract):

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
