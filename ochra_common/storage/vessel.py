from abc import abstractmethod
from dataclasses import dataclass
from .container import Container
from .reagent import Reagent


@dataclass
class Vessel(Container):
    capacity_unit: str
    reagents: list[Reagent]

    @abstractmethod
    def add_reagent(self, reagent: Reagent) -> None:
        pass

    @abstractmethod
    def remove_reagent(self, reagent: Reagent) -> None:
        pass
