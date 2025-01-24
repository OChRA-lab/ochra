from pydantic import Field
from ..base import DataModel
from .location import Location
from ..utils.enum import ActiveStatus
from ..storage.inventory import Inventory


class Station(DataModel):
    """
    Abstract station class that contains information all stations will have.

    Attributes:
        name (str): The name of the station.
        location (Location): The location of the station.
        status (ActiveStatus): The status of the station (e.g., idle, busy). Defaults to IDLE.
        locked_by (str): The user that has locked the station. Defaults to an empty string.
        inventory (Inventory): The inventory associated with the station.
    """

    name: str
    location: Location
    status: ActiveStatus = ActiveStatus.IDLE
    locked_by: str = Field(default="")
    inventory: Inventory = Field(default=None)

    _endpoint = "stations"  # associated endpoint for all stations
