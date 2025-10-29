from pydantic import Field
from typing import List
from .container import Container
from .reagent import Reagent


class Vessel(Container):
    """
    Represents a specialized container designed to store chemical reagents.
    """

    capacity_unit: str
    """Unit of measurement for the vessel's capacity (e.g., 'mL', 'L')."""

    reagents: List[Reagent] = Field(default_factory=list)
    """Collection of reagents currently held in the vessel."""

    def add_reagent(self, reagent: Reagent) -> None:
        """
        Add a reagent to the vessel.

        Args:
            reagent (Reagent): The reagent to be added.
        """
        raise NotImplementedError

    def remove_reagent(self, reagent: Reagent) -> None:
        """
        Remove a reagent from the vessel.

        Args:
            reagent (Reagent): The reagent to be removed.
        """
        raise NotImplementedError
