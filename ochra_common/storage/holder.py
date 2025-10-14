from pydantic import Field
from typing import List, Type
from .container import Container


class Holder(Container):
    """
    Represents a container capable of holding other containers, such as a rack of vials.

    Attributes:
        containers (List[Type[Container]]): List of containers currently held by this holder. Defaults to an empty list.
    """

    containers: List[Type[Container]] = Field(default_factory=list)

    def add_container(self, container: Type[Container]) -> None:
        """
        Add a container to the holder.

        Args:
            container (Type[Container]): The container to be added.
        """
        raise NotImplementedError

    def remove_container(self, container: Type[Container]) -> None:
        """
        Remove a container from the holder.

        Args:
            container (Type[Container]): The container to be removed.
        """
        raise NotImplementedError
