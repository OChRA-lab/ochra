from ..base import DataModel


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

    _endpoint = "storage"  # associated endpoint for all containers

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
