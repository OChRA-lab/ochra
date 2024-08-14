from abc import abstractmethod
from dataclasses import dataclass
from ..base import DataModel
from enum import Enum
from typing import Any


@dataclass
class Reagent(DataModel):
    """
    Abstract Reagent class to represent any chemicals used.

    Attributes:
        name (str): The name of the reagent.
        amount (float): The amount of the reagent.
        unit (str): The unit of measurement for the amount.
        physical_state (Enum): The physical state of the reagent (e.g., solid, liquid, gas).
        properties (dict): A dictionary of additional properties of the reagent.
    """
    name: str
    amount: float
    unit: str
    physical_state: Enum
    properties: dict

    @abstractmethod
    def add_property(self, property_name: str, property_value: Any) -> bool:
        """
        Add a property to the reagent.

        Args:
            property_name (str): The name of the property to add.
            property_value (Any): The value of the property to add.

        Returns:
            bool: True if the property was added successfully
        """
        pass

    @abstractmethod
    def remove_property(self, property: str) -> bool:
        """
        Remove a property from the reagent.

        Args:
            property (str): The name of the property to remove.

        Returns:
            bool: True if the property was removed successfully
        """
        pass

    @abstractmethod
    def change_amount(self, amount: float) -> bool:
        """
        Change the amount of the reagent.

        Args:
            amount (float): The new amount to set.

        Returns:
            bool: True if the amount was changed successfully
        """
        pass
