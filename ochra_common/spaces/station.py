from abc import ABC, abstractmethod
from dataclasses import dataclass
from ochra_common.base import DataModel
from ochra_common.spaces.location import Location
from ochra_common.storage.stock import Stock


@dataclass
class Station(DataModel, ABC):
    name: str
    location: Location
    stock: Stock
