from dataclasses import dataclass
from ..base import DataModel


@dataclass
class Location(DataModel):
    name: str
    map: str
    map_id: int
