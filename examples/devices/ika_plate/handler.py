from .abstract import IkaPlateAbstract
from ochra.common.utils.mixins import RestProxyMixin
from ochra.common.equipment.device import HTMLForm, CircularRangeInput
import logging
from typing import Annotated

logger = logging.getLogger(__name__)


class IkaPlate(IkaPlateAbstract, RestProxyMixin):
    def __init__(self, name):
        super().__init__(
            name=name, module_path="devices.ika_plate.device", collection="devices"
        )
        self._mixin_hook(self._endpoint, self.id)

    @HTMLForm(call="set_temperature", method="POST")
    def set_temperature(
        self,
        temperature: Annotated[
            int,
            CircularRangeInput(
                "Temperature",
                min="0",
                max="310",
                step="1",
                variable_binding="temperature",
            ),
        ],
    ) -> bool:
        self.temperature = temperature
        logger.info(f"set temperature to {temperature}")
        return True

    @HTMLForm(call="start_heat", method="POST")
    def start_heat(self) -> bool:
        logger.info("start heating")
        return True

    @HTMLForm(call="stop_heat", method="POST")
    def stop_heat(self) -> bool:
        logger.info("stop heating")
        return True

    @HTMLForm(call="set_speed", method="POST")
    def set_speed(
        self,
        speed: Annotated[
            int,
            CircularRangeInput(
                "Stir Speed",
                min="0",
                max="1500",
                step="1",
                variable_binding="stir_speed",
            ),
        ],
    ) -> bool:
        logger.info(f"set stir speed to {speed}")
        self.stir_speed = speed
        return True

    @HTMLForm(call="start_stir", method="POST")
    def start_stir(self) -> bool:
        logger.info("start stirring")
        return True

    @HTMLForm(call="stop_stir", method="POST")
    def stop_stir(self) -> bool:
        logger.info("stop stirring")
        return True
