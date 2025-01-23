from pydantic import Field
from ..base import DataModel
from .location import Location
from ..storage.inventory import Inventory
from uuid import UUID

class Station(DataModel):
    """
    Abstract station class that contains information all stations will have.

    Attributes:
        name (str): The name of the station.
        location (Location): The location of the station.
        stock (Stock): The stock associated with the station.
    """

    name: str
    location: Location
    inventory: Inventory = Field(default=None)
    locked: UUID = Field(defualt=None)

    _endpoint = "stations"  # associated endpoint for all stations

    def lock(self, session_id: UUID):
        """Lock the device for the given session."""
        if self.locked is not None:
            raise Exception(
                f"Device {self.name} is already locked by session {self.locked}."
            )
        else:
            self.locked = session_id

    def unlock(self, session_id: UUID):
        """Unlock the device for the given session."""
        if self.locked != session_id:
            raise Exception(
                f"Session {session_id} does not have lock on device {self.name}."
            )
        else:
            self.locked = None