from ochra_common.storage.vessel import Vessel
from ochra_common.utils.mixins import RestProxyMixin
from ochra_common.storage.reagent import Reagent


class Vessel(Vessel, RestProxyMixin):
    def __init__(self, type: str, max_capacity: float, capacity_unit: str):
        super().__init__(type=type, max_capacity=max_capacity,
                         capacity_unit=capacity_unit,
                         module_path="ochra_discovery.storage.vessel")
        self._mixin_hook(self._endpoint, self.id)

    def add_reagent(self, reagent: Reagent) -> None:
        reagents = self.reagents
        reagents.append(reagent)
        self.reagents = reagents

    def remove_reagent(self, reagent: Reagent) -> None:
        reagents = self.reagents
        reagents.remove(reagent)
        self.reagents = reagents
