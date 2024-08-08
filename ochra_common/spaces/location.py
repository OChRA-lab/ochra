from abc import ABC
from dataclasses import dataclass
from ochra_common.base import DataModel

@dataclass
class Location(DataModel,ABC):
    name: str
    map: str
    map_id: int