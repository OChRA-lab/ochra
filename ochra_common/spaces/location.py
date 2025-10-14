from pydantic import Field
from typing import List, Dict, Any
from ..base import DataModel


class Location(DataModel):
    """
    Represents a physical location within a laboratory environment.

    Attributes:
        lab (str): Name of the laboratory.
        room (str): Specific room or area within the laboratory.
        place (str): Precise spot within the room (e.g., bench, shelf, cabinet).
        landmarks (List[str]): Distinctive features or markers to help identify the location.
        additional_metadata (Dict[str, Any]): Supplementary metadata or contextual information about the location.
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
