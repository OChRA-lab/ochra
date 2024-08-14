from dataclasses import dataclass
from ..base import DataModel
from .location import Location
from ..storage.stock import Stock


@dataclass
class Station(DataModel):
    """
    Abstract station class that contains information all stations will have.

    Attributes:
        name (str): The name of the station.
        location (Location): The location of the station.
        stock (Stock): The stock associated with the station.
    """
    name: str
    location: Location
    stock: Stock
