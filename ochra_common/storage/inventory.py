from abc import ABC, abstractmethod
from dataclasses import dataclass
from ochra_common.base import DataModel
from ochra_common.storage.consumable import Consumable
from ochra_common.storage.container import Container

@dataclass
class Inventory(DataModel,ABC):
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