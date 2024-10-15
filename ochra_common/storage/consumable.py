from ..base import DataModel


class Consumable(DataModel):
    """
    Abstract class for lab consumables, such as caps, needles, etc.

    Attributes:
        type (str): The type of the consumable.
        quantity (int): The quantity of the consumable.
    """
    type: str
    quantity: int

    _endpoint = "storage/consumables"  # associated endpoint for all consumables

    def change_quantity(self, quantity: int) -> None:
        """
        Change the quantity of the consumable.

        Args:
            quantity (int): The new quantity to set.
        """
        raise NotImplementedError
