from dataclasses import dataclass
from ..base import DataModel
from .location import Location
from ..storage.stock import Stock


@dataclass
class Station(DataModel):
    name: str
    location: Location
    stock: Stock
