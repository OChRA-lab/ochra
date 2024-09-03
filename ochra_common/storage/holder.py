from pydantic import Field
from typing import List, Type
from .container import Container


class Holder(Container):
    """
    Abstract holder class, any container that can hold other containers.

    Attributes:
        containers (List[Container]): A list of containers held by this holder. Defaults to an empty list.
    """
    containers: List[Type[Container]] = Field(default_factory=list)

    def add_container(self, container: Type[Container]) -> None:
        """
        Add a container to the holder.

        Args:
            container (Container): The container to be added.
        """
        raise NotImplementedError

    def remove_container(self, container: Type[Container]) -> None:
        """
        Remove a container from the holder.

        Args:
            container (Container): The container to be removed.
        """
        raise NotImplementedError
