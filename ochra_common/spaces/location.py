from dataclasses import dataclass
from ..base import DataModel


@dataclass
class Location(DataModel):
    """
    Abstract location to correspond to a physical location.

    Attributes:
        name (str): The name of the location.
        map (str): The map associated with the location.
        map_id (int): The identifier for the map.
    """
    name: str
    map: str
    map_id: int
