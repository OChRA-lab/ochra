from ochra_common.equipment.device import Device
from ochra_common.equipment.temperature_control import TemperatureControls
from ochra_common.equipment.stir_control import StirControls
from pydantic import Field


class IkaPlateAbstract(Device, TemperatureControls, StirControls):
    temperature: float = Field(default=0)
    stir_speed: float = Field(default=0)
