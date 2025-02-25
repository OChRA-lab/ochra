from pydantic import Field
from typing import List
from uuid import UUID

from ochra_common.equipment.uigenerators import HypermediaBuilder

from ..base import DataModel
from .operation import Operation
from ..utils.enum import ActivityStatus
from ..storage.inventory import Inventory


# When an instance of the Device is made the DeciceMeta scans all attributes for _display_metadata and _form_metada
# It works the following way
# When a new instance of a Device (or Device ancestor) is being created
# Before that instance is created the metaclass is called
# It attaches two attributes to the new class _ui_states and _ui_forms
# For each attr_name and attr ke value pair in the new Device class
# if the attribute has the _display_metadata attribute then we register the name of that attribute in _ui_states for later use by the HypermediaBuilder
# if the attribute has the _form_metadata attribute then we register the name of that attribute in _ui_forms for later use by the HypermediaBuilder
class Device(DataModel):
    """
    Abstract device class that contains information all devices will have.

    Attributes:
        name (str): The name of the device.
        inventory (DeviceInventory): The inventory associated with the device.
        status (ActiveStatus): The current active status of the device. Defaults to IDLE.
        operation_history (List[Operation]): A list of operations performed by the device.
        owner_station (str): ID of the station which the device belongs to.
    """
    name: str
    inventory: Inventory = Field(default=None)
    status: ActivityStatus = ActivityStatus.IDLE
    operation_history: List[Operation] = Field(default_factory=list)
    owner_station: UUID = Field(default=None)

    _endpoint = "devices"  # associated endpoint for all devices
    _ui_states = []  # For @State attributes
    _ui_forms = []   # For @Form functions

    def __init_subclass__(cls, **kwargs):
        """Initialize subclass with UI element tracking"""
        super().__init_subclass__(**kwargs)
        
        # Initialize UI element tracking for the subclass
        cls._ui_states = []
        cls._ui_forms = []
        
        # Scan for decorated elements in the subclass
        for attr_name, attr in cls.__dict__.items():
            if hasattr(attr, '_display_metadata'):
                cls._ui_states.append(attr_name)
            elif hasattr(attr, '_form_metadata'):
                cls._ui_forms.append(attr_name)

    def to_html(self) -> str:
        """Public interface for HTML rendering"""
        return HypermediaBuilder(self).build()
