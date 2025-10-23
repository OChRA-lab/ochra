from pydantic import Field
from typing import List, Dict, Any
from ..base.data_model import DataModel


class Location(DataModel):
    """
    Represents a physical location within a laboratory environment.
    """

    lab: str
    """Name of the laboratory."""

    room: str = Field(default="")
    """Specific room or area within the laboratory."""

    place: str = Field(default="")
    """Precise spot within the room (e.g., bench, shelf, cabinet)."""

    landmarks: List[str] = Field(default_factory=list)
    """Distinctive features or markers to help identify the location."""

    additional_metadata: Dict[str, Any] = Field(default_factory=dict)
    """Supplementary metadata or contextual information about the location."""

    def __eq__(self, value: "Location") -> bool:
        return (
            value.lab == self.lab
            and value.room == self.room
            and value.place == self.place
        )
