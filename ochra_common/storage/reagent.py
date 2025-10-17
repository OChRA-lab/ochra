from pydantic import Field
from ..base import DataModel
from ..utils.enum import PhysicalState
from typing import Any, Dict


class Reagent(DataModel):
    """
    Represents a chemical reagent with associated metadata.
    """

    name: str
    """Name of the reagent."""

    amount: float
    """Quantity of the reagent."""
    
    unit: str
    """Unit of measurement for the amount (e.g., g, mL)."""
    
    physical_state: PhysicalState = PhysicalState.UNKNOWN
    """Physical state of the reagent (solid, liquid, gas, etc.). Defaults to UNKNOWN."""

    properties: Dict[str, Any] = Field(default_factory=dict)
    """Additional properties and metadata for the reagent."""

    _endpoint = "storage/reagents"  # associated endpoint for all reagents

    def add_property(self, property_name: str, property_value: Any) -> bool:
        """
        Add a property to the reagent.

        Args:
            property_name (str): The name of the property to add.
            property_value (Any): The value of the property to add.

        Returns:
            bool: True if the property was added successfully
        """
        raise NotImplementedError

    def remove_property(self, property: str) -> bool:
        """
        Remove a property from the reagent.

        Args:
            property (str): The name of the property to remove.

        Returns:
            bool: True if the property was removed successfully
        """
        raise NotImplementedError

    def change_amount(self, amount: float) -> bool:
        """
        Change the amount of the reagent.

        Args:
            amount (float): The new amount to set.

        Returns:
            bool: True if the amount was changed successfully
        """
        raise NotImplementedError
