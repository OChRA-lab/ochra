from ochra_common.storage.vessel import Vessel
from ochra_common.utils.mixins import RestProxyMixin
from ochra_common.storage.reagent import Reagent
from ochra_common.utils.enum import PatchType


class Vessel(Vessel, RestProxyMixin):
    def __init__(self, type: str, max_capacity: float, capacity_unit: str):
        """container that can hold reagents

        Args:
            type (str): type of vessel
            max_capacity (float): max capacity of the vessel
            capacity_unit (str): unit of the capacity
        """
        super().__init__(
            type=type,
            max_capacity=max_capacity,
            capacity_unit=capacity_unit,
            collection="containers",
            module_path="ochra_discovery.storage.vessel",
        )
        self._mixin_hook(self._endpoint, self.id)

    def add_reagent(self, reagent: Reagent) -> None:
        """add reagent to the vessel

        Args:
            reagent (Reagent): reagent to add
        """
        self._lab_conn.patch_property(self._endpoint, self.id, "reagents", reagent, PatchType.LIST_APPEND)

    def remove_reagent(self, reagent: Reagent) -> None:
        """remove reagent from the vessel

        Args:
            reagent (Reagent): reagent to remove
        """
        self._lab_conn.patch_property(self._endpoint, self.id, "reagents", reagent, PatchType.LIST_DELETE)
