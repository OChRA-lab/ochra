from dataclasses import dataclass
from ochra_common.base import DataModel


@dataclass
class Location(DataModel):
    name: str
    map: str
    map_id: int
