from pydantic import Field
from jinja2 import Environment, PackageLoader, select_autoescape
from typing import Annotated, Optional, List, Dict, Tuple, get_args, get_origin
from uuid import UUID
import inspect
from ..base import DataModel
from ..utils.enum import ActivityStatus
from ..storage.inventory import Inventory


# TODO: Solve problem whereby if the class you are using is the subclass of a subclass the generation does not work
# TODO: For example WebCamera <--inherits_from-- AbstractWebCamera <--inherits_from-- Device
# TODO: Rather than WebCamera <--inherits_from-- Device
# TODO: This might have to do with the deep chain of inheritance and maybe the HTML annotation work differently
class Device(DataModel):
    """
    Base class for all devices, providing common attributes. Instruments and robots are considered devices in our framework.

    Attributes:
        name (str): Device name.
        inventory (Inventory): Associated inventory object.
        status (ActivityStatus): Current operational status of the device (e.g., idle, busy), defaults to IDLE.
        owner_station (UUID): Station ID to which the device belongs.
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

        # Collect from all parent classes (except Device itself)
        for base in cls.__bases__:
            if hasattr(base, "_ui_states"):
                if isinstance(base._ui_states, list):
                    cls._ui_states.extend(getattr(base, "_ui_states", []))
            if hasattr(base, "_ui_forms"):
                if isinstance(base._ui_forms, list):
                    cls._ui_forms.extend(getattr(base, "_ui_forms", []))

        # Process class annotations
        for name, annotation in cls.__annotations__.items():
            if get_origin(annotation) is Annotated:
                for meta in get_args(annotation)[1:]:
                    if isinstance(meta, HTMLAttribute):
                        cls._ui_states.append((name, meta))

        # Process methods
        for name, attr in cls.__dict__.items():
            if inspect.isfunction(attr) and hasattr(attr, "_form_metadata"):
                cls._ui_forms.append((name, attr._form_metadata))

        return (cls._ui_states, cls._ui_forms)

    def to_html(self) -> str:
        """
        Converts the device instance into an HTML representation.
        Returns:
            str: The HTML string representing the device.
        """

        return HypermediaBuilder(self).build()


class HTMLAttribute:
    """
    Meta class for annotating variables to generate HTML attributes in UI rendering on the web app.

    Args:
        label (str): Human-readable label for the UI element.
        element (str): Type of HTML element (e.g., 'input', 'div', 'select').
        **attrs: Additional HTML attributes (e.g., placeholder, class, style).

    Usage:
        Use as metadata in Annotated type hints to describe how a field should appear in the UI.
    """

    def __init__(self, label: str, element: str, **attrs):
        """
        Initialize an HTMLAttribute instance.

        Args:
            label (str): Human-readable label for the UI element.
            element (str): Type of HTML element (e.g., 'input', 'div', 'select').
            **attrs: Additional HTML attributes (e.g., placeholder, class, style).
        """

        self.label = label
        self.element = element
        self.attrs = attrs


class HTMLInput:
    """
    Meta class for annotating function arguments to generate HTML inputs in UI rendering on the web app.

    Attributes:
        label (str): The label for the input element.
        type (str): The type of the input element (e.g., 'text', 'number').
        variable_binding (str): Optional variable binding for the input element.
        attrs (dict): Additional HTML attributes for the input element.

    Usage:
        Use as metadata in Annotated type hints to describe how a field should appear in the UI.
    """

    def __init__(self, label: str, type: str, variable_binding: str = "", **attrs):
        """
        Initialize an HTMLInput instance.

        Args:
            label (str): The label for the input element.
            type (str): The type of the input element (e.g., 'text', 'number').
            variable_binding (str, optional): The variable binding associated with the input element. Defaults to "".
            **attrs: Additional HTML attributes for the input element.
        """

        self.label = label
        self.type = type
        self.variable_binding = variable_binding
        self.attrs = attrs


class CircularRangeInput(HTMLInput):
    """
    Specialized HTMLInput for inputs that are represented as circular range sliders.
    """

    def __init__(self, unitname: str, min, max, step, variable_binding: str = ""):
        """
        Initializes a CircularRangeInput.
        Args:
            unitname (str): The label or name of the unit.
            min: The minimum value of the range.
            max: The maximum value of the range.
            step: The step size for the range.
            variable_binding (str, optional): The variable binding associated with the input element. Defaults to "".
        """
        self.label = unitname
        self.type = "custom_circular_range"
        self.variable_binding = variable_binding
        self.attrs = {"min": min, "max": max, "step": step}


# This decorator marks a function as a form for calling methods
class HTMLForm:
    """
    Decorator class to annotate methods as HTML forms for UI rendering on the web app.

    Attributes:
        call (str): The endpoint or action to call when the form is submitted.
        method (str): The HTTP method to use (e.g., 'POST', 'GET').
        action (str): Optional action URL for the form submission.
    """

    def __init__(self, call: str, method: str, action: str = ""):
        """
        Initialize an HTMLForm instance.
        Args:
            call (str): The endpoint or action to call when the form is submitted.
            method (str): The HTTP method to use (e.g., 'POST', 'GET').
            action (str, optional): Optional action URL for the form submission. Defaults to "".
        """
        self.call = call
        self.method = method
        self.action = action

    def __call__(self, func):
        """
        Call the decorator.
        """
        params = {}
        sig = inspect.signature(func)
        for name, param in sig.parameters.items():
            if name == "self":
                continue
            if get_origin(param.annotation) is Annotated:
                for meta in get_args(param.annotation)[1:]:
                    if isinstance(meta, HTMLInput):
                        params[name] = meta
        func._form_metadata = {
            "call": self.call,
            "method": self.method,
            "action": self.action,
            "params": params,
        }
        return func


class HypermediaBuilder:
    """
    Builds HTML representation of a Device instance using Jinja2 templates.
    
    Attributes:
        device (Device): The device instance to be represented.
        env (Environment): Jinja2 environment for template rendering.
    """
    def __init__(self, device: Device):
        self.device = device
        self.env = Environment(
            # Loads templates from "templates" directory
            # inside "your_package_name" Python package
            loader=PackageLoader("ochra_common", "templates"),
            # Auto-escape HTML for safety
            autoescape=select_autoescape(),
        )

        # Make macros available globally
        self.env.globals.update(
            {
                "state_macro": self.env.get_template(
                    "components.html"
                ).module.state_macro,
                "state_chip": self.env.get_template(
                    "components.html"
                ).module.state_chip,
                "form_macro": self.env.get_template(
                    "components.html"
                ).module.form_macro,
                "circular_range": self.env.get_template(
                    "components.html"
                ).module.circular_range,
            }
        )

    def build(self) -> str:
        """
        Renders the HTML representation of the device using Jinja2 templates.
        Returns:
            str: The rendered HTML string.
        """
        template = self.env.get_template("device_base.html")

        context = {
            "states": self._get_state_context(),
            "forms": self._get_form_context(),
            "device": self.device,  # Pass full device instance for custom templates
            "station_id": self.device.owner_station,  # Assuming that the oewner_station is set
        }

        return template.render(context)

    def _get_state_context(self) -> List[Dict]:
        """
        Builds the context for rendering device states.

        Returns:
            List[Dict]: A list of dictionaries representing state metadata and values.
        """
        return [
            {"name": name, "value": getattr(self.device, name), "meta": meta}
            for name, meta in self.device._ui_states
        ]

    def _get_form_context(self) -> List[Dict]:
        """
        Builds the context for rendering device forms.
        
        Returns:
            List[Dict]: A list of dictionaries representing form metadata and parameters.
        """
        forms = []
        for _, meta in self.device._ui_forms:
            params = {}
            for name, input_meta in meta["params"].items():
                attributes = dict(
                    input_meta.attrs
                )  # Copying to avoid mutating original dict

                # Insert dynamic dropdown options if available for 'task_list' parameter
                if name == "task_name" and hasattr(self.device, "available_tasks"):
                    attributes["options"] = self.device.available_tasks

                params[name] = {
                    "name": name,
                    "label": input_meta.label,
                    "type": input_meta.type,
                    "variable_binding": getattr(
                        self.device, input_meta.variable_binding
                    )
                    if hasattr(self.device, input_meta.variable_binding)
                    else "",
                    "attrs": attributes,
                }
            forms.append(
                {
                    "call": meta["call"],
                    "method": meta["method"],
                    "action": meta["action"],
                    "params": params,
                }
            )

        # TODO: Write documentation on the variable binding

        return forms
