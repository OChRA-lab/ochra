from ochra.common.equipment.device import Device, HTMLAttribute
from pydantic import Field
from typing import Annotated


class TecanXCaliburAbstract(Device):
    reagents_map: Annotated[
        dict,
        Field(default_factory=dict),
        HTMLAttribute(label="reagents_map", element="li"),
    ]
