from dataclasses import dataclass
from .station import Station


@dataclass
class StorageStation(Station):
    """Station abstract purely for storage"""
    pass
