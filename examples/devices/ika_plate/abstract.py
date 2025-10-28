from typing import Annotated
from ochra.common.equipment.device import Device, HTMLAttribute
from pydantic import Field


class IkaPlateAbstract(Device):
    temperature: Annotated[
        int, Field(default=0), HTMLAttribute(label="Temperature", element="li")
    ]
    stir_speed: Annotated[
        int, Field(default=0), HTMLAttribute(label="Stir Speed", element="li")
    ]
