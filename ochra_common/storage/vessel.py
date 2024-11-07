from pydantic import Field
from typing import List
from .container import Container
from .reagent import Reagent


class Vessel(Container):
    """
    Vessel Abstract class, any container that can hold reagents.

    Attributes:
        capacity_unit (str): The unit of measurement for the vessel's capacity.
        reagents (List[Reagent]): A list of reagents contained in the vessel. Defaults to an empty list.
    """

    capacity_unit: str
    reagents: List[Reagent] = Field(default_factory=list)

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
