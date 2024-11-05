from ochra_common.storage.reagent import Reagent
from ochra_common.utils.mixins import RestProxyMixin
from typing import Any


class Reagent(Reagent, RestProxyMixin):
    def __init__(self, name: str, amount: float, unit: str):
        super().__init__(
            name=name,
            amount=amount,
            unit=unit,
            module_path="ochra_discovery.storage.reagent",
        )
        self._mixin_hook(self._endpoint, self.id)

    def add_property(self, property_name: str, property_value: Any) -> bool:
        properties = self.properties
        properties.update({property_name: property_value})
        self.properties = properties
        return True

    def remove_property(self, property_name: str) -> bool:
        properties = self.properties
        properties.pop(property_name, None)
        self.properties = properties
        return True

    def change_amount(self, amount: float) -> bool:
        self.amount = amount
        return True
