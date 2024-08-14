from dataclasses import dataclass
from .station import Station


@dataclass
class StorageStation(Station):
    """
    StorageStation abstract class that represents a station purely for storage purposes.
    """
    pass
