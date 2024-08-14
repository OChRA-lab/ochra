from abc import abstractmethod
from dataclasses import dataclass
from .container import Container


@dataclass
class Holder(Container):
    """
    Abstract holder class, any container that can hold other containers.

    Attributes:
        containers (list[Container]): A list of containers held by this holder.
    """
    containers: list[Container]

    @abstractmethod
    def add_container(self, container: Container) -> None:
        """
        Add a container to the holder.

        Args:
            container (Container): The container to be added.
        """
        pass

    @abstractmethod
    def remove_container(self, container: Container) -> None:
        """
        Remove a container from the holder.

        Args:
            container (Container): The container to be removed.
        """
        pass
