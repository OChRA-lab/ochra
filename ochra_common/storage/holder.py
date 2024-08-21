from abc import abstractmethod
from dataclasses import dataclass, field
from typing import List
from .container import Container


@dataclass(kw_only=True)
class Holder(Container):
    """
    Abstract holder class, any container that can hold other containers.

    Attributes:
        containers (List[Container]): A list of containers held by this holder. Defaults to an empty list.
    """
    containers: List[Container] = field(default_factory=list)

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
