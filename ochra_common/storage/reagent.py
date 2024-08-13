from abc import abstractmethod
from dataclasses import dataclass
from ..base import DataModel
from enum import Enum
from typing import Any


@dataclass
class Reagent(DataModel):
    name: str
    amount: float
    unit: str
    physical_state: Enum
    properties: dict

    @abstractmethod
    def add_property(self, property_name: str, property_value: Any) -> bool:
        pass

    @abstractmethod
    def remove_property(self, property: str) -> bool:
        pass

    @abstractmethod
    def change_amount(self, amount: float) -> bool:
        pass
