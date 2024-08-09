from abc import ABC, abstractmethod
from dataclasses import dataclass
from ochra_common.base import DataModel
from ochra_common.spaces.location import Location
from ochra_common.spaces.station import Station
from ochra_common.equipment.device import Device


@dataclass
class StorageStation(Station, ABC):
    pass
