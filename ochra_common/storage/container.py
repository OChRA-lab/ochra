from abc import ABC, abstractmethod
from dataclasses import dataclass
from ochra_common.base import DataModel

@dataclass
class Container(DataModel,ABC):
    type: str
    is_used: bool
    physical_id: int
    max_capacity: int

    @abstractmethod
    def get_used_capacity(self) -> float|int:
        pass

    @abstractmethod
    def get_available_capacity(self) -> float|int:
        pass