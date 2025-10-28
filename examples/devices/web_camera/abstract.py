from ochra.common.equipment.device import Device, HTMLAttribute
from pydantic import Field
from typing import Annotated


class WebCameraAbstract(Device):
    usb_port: Annotated[
        str, Field(default=""), HTMLAttribute(label="USB Port", element="li")
    ]
