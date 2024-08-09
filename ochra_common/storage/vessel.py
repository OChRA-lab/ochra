from abc import ABC, abstractmethod
from dataclasses import dataclass
from ochra_common.base import DataModel
from ochra_common.storage.container import Container
from ochra_common.storage.reagent import Reagent


@dataclass
class Vessel(Container, ABC):
    capacity_unit: str
    reagents: list[Reagent]

    @abstractmethod
    def add_reagent(self, reagent: Reagent) -> None:
        pass

    @abstractmethod
    def remove_reagent(self, reagent: Reagent) -> None:
        pass
