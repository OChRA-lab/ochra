from dataclasses import dataclass
from ..base import DataModel
from .location import Location
from ..storage.stock import Stock


@dataclass
class Station(DataModel):
    """Abstract station class that contains information all stations will have"""
    name: str
    location: Location
    stock: Stock
