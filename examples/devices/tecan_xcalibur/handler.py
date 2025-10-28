from .abstract import TecanXCaliburAbstract
from ochra.common.utils.mixins import RestProxyMixin
from ochra.common.equipment.device import HTMLForm, HTMLInput
from typing import Dict, Any, Annotated
from time import sleep
import logging

logger = logging.getLogger(__name__)


class TecanXCalibur(TecanXCaliburAbstract, RestProxyMixin):
    def __init__(self, name: str, reagents_map: Dict[str, Any]):
        super().__init__(
            name=name,
            reagents_map=reagents_map,
            module_path="devices.tecan_xcalibur.device",
            collection="devices",
        )
        self._mixin_hook(self._endpoint, self.id)

    @HTMLForm(call="dispense", method="POST")
    def dispense(
        self,
        reagent: Annotated[
            str, HTMLInput("Reagent name", "text", variable_binding="reagent")
        ],
        volume: Annotated[
            int, HTMLInput("volume", "number", variable_binding="volume")
        ],
        unit: Annotated[str, HTMLInput("Unit", "text", variable_binding="unit")],
    ) -> bool:
        if reagent in self.reagents_map:
            logger.info(f"dispensing {volume} {unit} of {reagent}")
            sleep(2)
            return True
        else:
            logger.error(f"{reagent} not found in reagents map")
            return False
