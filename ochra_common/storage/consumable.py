from abc import ABC, abstractmethod
from dataclasses import dataclass
from ochra_common.base import DataModel


@dataclass
class Consumable(DataModel, ABC):
    type: str
    quantity: int

    @abstractmethod
    def change_quantity(self, quantity: int) -> None:
        pass
