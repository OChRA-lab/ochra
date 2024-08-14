from abc import abstractmethod
from dataclasses import dataclass
from .container import Container
from .reagent import Reagent


@dataclass
class Vessel(Container):
    """
    Vessel Abstract class, any container that can hold reagents.

    Attributes:
        capacity_unit (str): The unit of measurement for the vessel's capacity.
        reagents (list[Reagent]): A list of reagents contained in the vessel.
    """
    capacity_unit: str
    reagents: list[Reagent]

    @abstractmethod
    def add_reagent(self, reagent: Reagent) -> None:
        """
        Add a reagent to the vessel.

        Args:
            reagent (Reagent): The reagent to be added.
        """
        pass

    @abstractmethod
    def remove_reagent(self, reagent: Reagent) -> None:
        """
        Remove a reagent from the vessel.

        Args:
            reagent (Reagent): The reagent to be removed.
        """
        pass
