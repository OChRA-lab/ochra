from abc import abstractmethod
from dataclasses import dataclass
from ..base import DataModel


@dataclass
class Consumable(DataModel):
    type: str
    quantity: int

    @abstractmethod
    def change_quantity(self, quantity: int) -> None:
        pass
