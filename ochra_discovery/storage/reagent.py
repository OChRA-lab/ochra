from ochra_common.storage.reagent import Reagent
from ochra_common.utils.mixins import RestProxyMixin
from typing import Any


class Reagent(Reagent, RestProxyMixin):
    def __init__(self, name: str, amount: float, unit: str):
        """Reagent object that represents a reagent in the lab

        Args:
            name (str): name of reagent
            amount (float): amount of reagent
            unit (str): unit of the amount
        """
        super().__init__(
            name=name,
            amount=amount,
            unit=unit,
            collection="reagents",
            module_path="ochra_discovery.storage.reagent",
        )
        self._mixin_hook(self._endpoint, self.id)

    def add_property(self, property_name: str, property_value: Any) -> bool:
        """adds a property to the reagent, just for notes

        Args:
            property_name (str): property name
            property_value (Any): property value

        """
        properties = self.properties
        properties.update({property_name: property_value})
        self.properties = properties
        return True

    def remove_property(self, property_name: str) -> bool:
        """removes a property from the reagent

        Args:
            property_name (str): property name to remove

        Returns:
            bool: returns True if successful
        """
        properties = self.properties
        properties.pop(property_name, None)
        self.properties = properties
        return True

    def change_amount(self, amount: float) -> bool:
        """changes the amount of the reagent

        Args:
            amount (float): new amount of the reagent

        Returns:
            bool: returns True if successful
        """
        self.amount = amount
        return True
