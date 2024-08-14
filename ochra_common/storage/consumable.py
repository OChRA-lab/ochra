from abc import abstractmethod
from dataclasses import dataclass
from ..base import DataModel


@dataclass
class Consumable(DataModel):
    """Abstract for lab consumables, (caps, needles, etc)"""
    type: str
    quantity: int

    @abstractmethod
    def change_quantity(self, quantity: int) -> None:
        pass
