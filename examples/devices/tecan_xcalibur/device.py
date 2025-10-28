from .abstract import TecanXCaliburAbstract
from ochra.common.utils.mixins import RestProxyMixinReadOnly


class TecanXCalibur(TecanXCaliburAbstract, RestProxyMixinReadOnly):
    def __init__(self, name):
        super().__init__()
        self._mixin_hook(self._endpoint, name)

    def dispense(self, reagent: str, volume: int, unit: str) -> bool:
        return self._lab_conn.call_on_object(
            self._endpoint,
            self.id,
            "dispense",
            {"reagent": reagent, "volume": volume, "unit": unit},
        )
