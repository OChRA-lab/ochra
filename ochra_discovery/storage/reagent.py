from ochra_common.storage.reagent import Reagent
from ochra_common.utils.mixins import RestProxyMixin
from ochra_common.utils.enum import PatchType
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
        self._lab_conn.patch_property(self._endpoint, self.id, "properties", property_value, PatchType.DICT_INSERT, {"key": property_name})
        return True

    def remove_property(self, property_name: str) -> bool:
        """removes a property from the reagent

        Args:
            property_name (str): property name to remove

        Returns:
            bool: returns True if successful
        """
        self._lab_conn.patch_property(self._endpoint, self.id, "properties", None, PatchType.DICT_DELETE, {"key": property_name})
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
