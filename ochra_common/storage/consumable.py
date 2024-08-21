from abc import abstractmethod
from dataclasses import dataclass
from ..base import DataModel

_COLLECTION = "consumables"


@dataclass(kw_only=True)
class Consumable(DataModel):
    """
    Abstract class for lab consumables, such as caps, needles, etc.

    Attributes:
        type (str): The type of the consumable.
        quantity (int): The quantity of the consumable.
    """
    type: str
    quantity: int

    def __post_init__(self):
        self._collection = _COLLECTION
        return super().__post_init__()

    @abstractmethod
    def change_quantity(self, quantity: int) -> None:
        """
        Change the quantity of the consumable.

        Args:
            quantity (int): The new quantity to set.
        """
        pass
