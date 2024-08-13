from abc import abstractmethod
from dataclasses import dataclass
from ochra_common.storage.container import Container


@dataclass
class Holder(Container):
    containers: list[Container]

    @abstractmethod
    def add_container(self, container: Container) -> None:
        pass

    @abstractmethod
    def remove_container(self, container: Container) -> None:
        pass
