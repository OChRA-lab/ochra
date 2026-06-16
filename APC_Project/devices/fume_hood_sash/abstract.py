from typing import Annotated

from ochra.common.equipment.device import Device, HTMLAttribute
from pydantic import Field


class FumeHoodSash(Device):
    """Shared OChRA-facing state for the Opta-backed fume hood sash."""

    connection_mode: Annotated[
        str, Field(default="tcp"), HTMLAttribute(label="Connection Mode", element="li")
    ]
    address: Annotated[
        str, Field(default="192.168.1.53"), HTMLAttribute(label="IP Address", element="li")
    ]
    port: Annotated[
        int, Field(default=5000), HTMLAttribute(label="TCP Port", element="li")
    ]
    simulation_enabled: Annotated[
        bool, Field(default=False), HTMLAttribute(label="Simulation", element="li")
    ]
    connected: Annotated[
        bool, Field(default=False), HTMLAttribute(label="Connected", element="li")
    ]
    piston_up: Annotated[
        bool, Field(default=False), HTMLAttribute(label="Piston Up", element="li")
    ]
    sash_up: Annotated[
        bool, Field(default=False), HTMLAttribute(label="Sash Up", element="li")
    ]
    last_command: Annotated[
        str | None, Field(default=None), HTMLAttribute(label="Last Command", element="li")
    ]
    last_reply: Annotated[
        str | None, Field(default=None), HTMLAttribute(label="Last Reply", element="li")
    ]
    last_error: Annotated[
        str, Field(default=""), HTMLAttribute(label="Last Error", element="li")
    ]
