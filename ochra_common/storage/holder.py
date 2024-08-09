from abc import ABC, abstractmethod
from dataclasses import dataclass
from ochra_common.base import DataModel
from ochra_common.storage.container import Container


@dataclass
class Holder(Container, ABC):
    containers: list[Container]

    @abstractmethod
    def add_container(self, container: Container) -> None:
        pass

    @abstractmethod
    def remove_container(self, container: Container) -> None:
        pass
