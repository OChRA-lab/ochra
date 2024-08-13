from abc import abstractmethod
from dataclasses import dataclass
from ..base import DataModel
from .consumable import Consumable
from .container import Container


@dataclass
class Inventory(DataModel):
    containers: list[Container]
    consumables: list[Consumable]
    containers_max_capacity: int

    @abstractmethod
    def add_container(self, container: Container) -> None:
        pass

    @abstractmethod
    def remove_container(self, container: Container) -> None:
        pass

    @abstractmethod
    def add_consumable(self, consumable: Consumable) -> None:
        pass

    @abstractmethod
    def remove_consumable(self, consumable: Consumable) -> None:
        pass
