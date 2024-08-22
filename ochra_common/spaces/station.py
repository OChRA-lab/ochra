from dataclasses import dataclass
from ..base import DataModel
from .location import Location
from ..storage.stock import Stock

_COLLECTION = "stations"


@dataclass(kw_only=True)
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
    stock: Stock = None

    def __post_init__(self):
        self._collection = _COLLECTION
        return super().__post_init__()
