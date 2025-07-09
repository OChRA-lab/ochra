from pydantic import Field
from jinja2 import Environment, PackageLoader, select_autoescape
from typing import Annotated, Optional, Tuple, get_args, get_origin, List
from uuid import UUID
import inspect
from ..base import DataModel
from .operation import Operation
from ..utils.enum import ActivityStatus
from ..storage.inventory import Inventory





# TODO: Solve problem whereby if the class you are using is the subclass of a subclass the generation does not work
# TODO: For example WebCamera <--inherits_from-- AbstractWebCamera <--inherits_from-- Device
# TODO: Rather than WebCamera <--inherits_from-- Device
# TODO: This might have to do with the deep chain of inheritance and maybe the HTML annotation work differently
class Device(DataModel):
    """
    Abstract device class that contains information all devices will have.

    Attributes:
        name (str): The name of the device.
        inventory (DeviceInventory): The inventory associated with the device.
        status (ActiveStatus): The current active status of the device. Defaults to IDLE.
        owner_station (str): ID of the station which the device belongs to.
    """
    name: str
    inventory: Inventory = Field(default=None)
    status: ActivityStatus = ActivityStatus.IDLE
    owner_station: UUID = Field(default=None)
    _endpoint = "devices"
    _ui_states = []
    _ui_forms = []

    def __init_subclass__(cls, **kwargs) -> Optional[Tuple[list, list]]:
        super().__init_subclass__(**kwargs)
        
        cls._ui_states = []
        cls._ui_forms = []
        print(cls._ui_states)

        # Collect from all parent classes (except Device itself)
        for base in cls.__bases__:
            if hasattr(base, '_ui_states'):
                if isinstance(base._ui_states, list):
                    cls._ui_states.extend(getattr(base, '_ui_states', []))
            if hasattr(base, '_ui_forms'):
                if isinstance(base._ui_forms, list):
                    cls._ui_forms.extend(getattr(base, '_ui_forms', []))


        # Process class annotations
        for name, annotation in cls.__annotations__.items():
            if get_origin(annotation) is Annotated:
                for meta in get_args(annotation)[1:]:
                    if isinstance(meta, HTMLAttribute):
                        cls._ui_states.append((name, meta))
        
        # Process methods
        for name, attr in cls.__dict__.items():
            if inspect.isfunction(attr) and hasattr(attr, '_form_metadata'):
                cls._ui_forms.append((name, attr._form_metadata))


        return (cls._ui_states, cls._ui_forms)

    def to_html(self) -> str:
        return HypermediaBuilder(self).build()




# This meta class annotates variables to produce
class HTMLAttribute:
    def __init__(self, label: str, element: str, **attrs):
        self.label = label
        self.element = element
        self.attrs = attrs

# This meta class annotates function arguments for making input elements
class HTMLInput:
    def __init__(self, label: str, type: str, variable_binding: str = "", **attrs):
        self.label = label
        self.type = type
        self.variable_binding = variable_binding
        self.attrs = attrs


class CircularRangeInput(HTMLInput):
    def __init__(self, unitname: str, min, max, step, variable_binding: str = ""):
        self.label = unitname
        self.type = "custom_circular_range"
        self.variable_binding = variable_binding
        self.attrs = {"min": min, "max": max,"step": step}

# This decorator marks a function as a form for calling methods
class HTMLForm:
    def __init__(self, call: str, method: str, action: str = ""):
        self.call = call
        self.method = method
        self.action = action

    def __call__(self, func):
        params = {}
        sig = inspect.signature(func)
        for name, param in sig.parameters.items():
            if name == 'self':
                continue
            if get_origin(param.annotation) is Annotated:
                for meta in get_args(param.annotation)[1:]:
                    if isinstance(meta, HTMLInput):
                        params[name] = meta
        func._form_metadata = {
            'call': self.call,
            'method': self.method,
            'action': self.action,
            'params': params
        }
        return func


class HypermediaBuilder:
    def __init__(self, device: Device):
        self.device = device
        self.env = Environment(
            # Loads templates from "templates" directory 
            # inside "your_package_name" Python package
            loader=PackageLoader("ochra_common", "templates"),
            
            # Auto-escape HTML for safety
            autoescape=select_autoescape()
        )
        
        # Make macros available globally
        self.env.globals.update({
            'state_macro': self.env.get_template("components.html").module.state_macro,
            'state_chip': self.env.get_template("components.html").module.state_chip,
            'form_macro': self.env.get_template("components.html").module.form_macro,
            'circular_range': self.env.get_template("components.html").module.circular_range
        })

    def build(self) -> str:
        template = self.env.get_template("device_base.html")
        print(self._get_form_context())
        
        context = {
            "states": self._get_state_context(),
            "forms": self._get_form_context(),
            "device": self.device  # Pass full device instance for custom templates
        }
        
        return template.render(context)

    def _get_state_context(self):
        return [
            {
                "name": name,
                "value": getattr(self.device, name),
                "meta": meta
            }
            for name, meta in self.device._ui_states
        ]
        
    def _get_form_context(self):
        forms = []
        for _, meta in self.device._ui_forms:
            params = {}
            for name, input_meta in meta['params'].items():
                attributes = dict(input_meta.attrs)  # Copying to avoid mutating original dict

                # Insert dynamic dropdown options if available for 'task_list' parameter
                if name == "task_name" and hasattr(self.device, 'available_tasks'):
                    attributes['options'] = self.device.available_tasks
                
                params[name] = {
                    "name": name,
                    "label": input_meta.label,
                    "type": input_meta.type,
                    "variable_binding": getattr(self.device, input_meta.variable_binding) if hasattr(self.device, input_meta.variable_binding) else "",
                    "attrs": attributes
                }
            forms.append({
                "call": meta['call'],
                "method": meta['method'],
                "action": meta['action'],
                "params": params
            })
        
        # TODO: Write documentation on the variable binding 

        return forms
