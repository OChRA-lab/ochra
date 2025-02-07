from pydantic import Field
from typing import List, Dict, Any
from ..base import DataModel


class Location(DataModel):
    """
    Abstract location to correspond to a physical location.

    Attributes:
        name (str): The name of the location.
        map (str): The map associated with the location.
        map_id (int): The identifier for the location on the map.
    """

    lab: str
    room: str = Field(default="")
    place: str = Field(default="")
    landmarks: List[str] = Field(default_factory=list)
    additional_metadata: Dict[str, Any] = Field(default_factory=dict)

    def __eq__(self, value: "Location") -> bool:
        return (
            value.lab == self.lab
            and value.room == self.room
            and value.place == self.place
        )
