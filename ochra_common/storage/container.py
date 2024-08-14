from abc import abstractmethod
from dataclasses import dataclass
from ..base import DataModel


@dataclass
class Container(DataModel):
    """
    Abstract class for containers, anything that can hold something.

    Attributes:
        type (str): The type of the container.
        is_used (bool): Indicates whether the container has been used.
        physical_id (int): The physical identifier of the container.
        max_capacity (int): The maximum capacity of the container.
    """
    type: str
    is_used: bool
    physical_id: int
    max_capacity: int

    @abstractmethod
    def get_used_capacity(self) -> float | int:
        """
        Get the used capacity of the container.

        Returns:
            float | int: The used capacity of the container.
        """
        pass

    @abstractmethod
    def get_available_capacity(self) -> float | int:
        """
        Get the available capacity of the container.

        Returns:
            float | int: The available capacity of the container.
        """
        pass
