from dataclasses import dataclass
from ..base import DataModel


@dataclass
class Location(DataModel):
    """Abstract location to correspond to a physical location"""
    name: str
    map: str
    map_id: int
