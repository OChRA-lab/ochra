from ..base import DataModel


class Consumable(DataModel):
    """
    Data model for laboratory consumables (e.g., caps, needles).

    Attributes:
        type (str): Consumable category or name.
        quantity (int): Available quantity in inventory.
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
