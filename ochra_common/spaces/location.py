from abc import ABC
from dataclasses import dataclass, asdict
from ocrha_common.base import DataModel

@dataclass
class Location(DataModel,ABC):
    name: str
    map: str
    map_id: int