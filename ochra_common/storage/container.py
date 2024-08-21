from abc import abstractmethod
from dataclasses import dataclass
from ..base import DataModel

_COLLECTION = "containers"


@dataclass(kw_only=True)
class Container(DataModel):
    """
    Abstract class for containers, anything that can hold something.

    Attributes:
        type (str): The type of the container.
        max_capacity (int|float): The maximum capacity of the container.
        physical_id (int): The physical identifier of the container. Defaults to None.
        is_used (bool): Indicates whether the container has been used. Defaults to False.
    """
    type: str
    max_capacity: int | float
    physical_id: int = None
    is_used: bool = False

    def __post_init__(self):
        self._collection = _COLLECTION
        return super().__post_init__()

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
