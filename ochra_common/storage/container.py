from ..base import DataModel
from typing import Union


class Container(DataModel):
    """
    Abstract base class for a storage container that can hold other containers or reagents.

    Attributes:
        type (str): Type of the container (e.g., rack, vial, jar).
        max_capacity (int | float): Maximum capacity of the container.
        physical_id (int, optional): Unique physical identifier for the container. Defaults to None.
        is_used (bool, optional): Flag indicating if the container is in use. Defaults to False.
    """

    type: str
    max_capacity: int | float
    physical_id: int = None
    is_used: bool = False

    _endpoint = "storage/containers"  # associated endpoint for all containers

    def get_used_capacity(self) -> float | int:
        """
        Get the used capacity of the container.

        Returns:
            float | int: The used capacity of the container.
        """
        raise NotImplementedError

    def get_available_capacity(self) -> float | int:
        """
        Get the available capacity of the container.

        Returns:
            float | int: The available capacity of the container.
        """
        raise NotImplementedError
