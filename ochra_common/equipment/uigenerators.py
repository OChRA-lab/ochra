from dataclasses import dataclass
from pathlib import Path
from inspect import signature, Parameter
from typing import Any, Callable, Dict, List, Optional
import jinja2


@dataclass
class FormMetadata:
    command: str
    method: str
    params: List[Dict[str, type]]
    
@dataclass
class DisplayMetadata:
    name: str
    transformation: Callable[[Any], str]


class HTMLStateMetadata:
    """Class-based decorator to attach form metadata to methods"""
    def __init__(self, value_label: Optional[str] = None, transformation_function: Callable[[Any], str] = lambda x: str(x)):
        self.t_func = transformation_function
        self.value_label = value_label

    def __call__(self, func: Callable) -> Callable:
        """This makes the class instance act as the decorator"""
        func._display_metadata = DisplayMetadata(
            name =self.value_label or func.__name__,
            transformation=self.t_func
        )

        return func


class HTMLFormMetadata:
    """Class-based decorator to attach form metadata to methods""" 
    def __init__(self, command: str, method: str = "POST"):
        self.command = command
        self.method = method

    def __call__(self, func: Callable) -> Callable:
        """This makes the class instance act as the decorator"""
        
        # Extract parameter metadata from function signature
        sig = signature(func)
        params = [
            {
                "name": param.name,
                "type": param.annotation if param.annotation != Parameter.empty else str
            }
            for param in sig.parameters.values()
            if param.name != 'self'  # Exclude 'self' from form params
        ]

        func._form_metadata = FormMetadata(
            command = self.command,
            method = self.method,
            params = params
        )

        return func



class TerminalLogger:
    """Renders device information for the terminal for when you want to inspect rendering"""
    def __init__(self, device) -> None:
        self.device = device

    def build(self) -> str:
        return f"""
        <div id={self.device.id} class="iotdevice">
            <h1>{self.device.name}</h1>
            {self._build_states()}
            {self._build_forms()}
        </div>
        """

    def _build_states(self) -> str:
        ATTRIBUTES = []
        for attr in self.device._ui_states:
            GETTER_FUNC = getattr(self.device, attr) 
            GETTER_FUNC_METADATA: DisplayMetadata = GETTER_FUNC._display_metadata
            ATTRIBUTES.append(
                f"""
                <div class='state'>
                    <span>{GETTER_FUNC_METADATA.name}</span> : {GETTER_FUNC_METADATA.transformation(GETTER_FUNC())}
                </div>"""
            )

        return f"""
            <div class="states">
                {"\n\t\t".join(ATTRIBUTES)}
            </div>
        """


    def _build_forms(self) -> str:
        FORMS = []
        for attr in self.device._ui_forms:
            CONTROL_FUNC_METADATA: FormMetadata = getattr(self.device, attr)._form_metadata
            INPUTS = []
            for INPUT in CONTROL_FUNC_METADATA.params:
                INPUTS.append(
                f"""<label>
                        {INPUT["name"].capitalize()}
                        <input name='{INPUT["name"]}' type='text'/>
                    </label>"""
                )
            FORMS.append(
                f"""
                <form method="{CONTROL_FUNC_METADATA.method}", action={CONTROL_FUNC_METADATA.command}>
                    {'"\n\t\t    '.join(INPUTS)}
                </form>
                """
            )

        return f"""
            <div class="controls">
                {"\n\t\t".join(FORMS)}
            </div>
        """



class HypermediaBuilder:
    """Renders device UI using Jinja2 templates."""
    def __init__(self, device):
        module_dir = Path(__file__).resolve().parent
        self.device = device
        self.env = jinja2.Environment(
            loader=jinja2.FileSystemLoader(searchpath=module_dir),
            autoescape=True
        )
        self.template = self.env.get_template("device.html")

    def build(self) -> str:
        """Renders the full template with all UI components"""
        return self.template.render(
            states=self._build_states(),
            forms=self._build_forms(),
            device_name=self.device.name,
            device_id=self.device.id
        )

    def _build_states(self) -> List[Dict[str, Any]]:
        """Collects all state display metadata"""
        states = []
        
        for attr in self.device._ui_states:
            getter = getattr(self.device, attr)
            metadata: DisplayMetadata = getter._display_metadata
            
            states.append({
                'name': metadata.name,
                'value': metadata.transformation(getter()),
            })
            
        return states

    def _build_forms(self) -> List[Dict[str, Any]]:
        """Collects all form action metadata"""
        forms = []
        
        for attr in self.device._ui_forms:
            metadata: FormMetadata = getattr(self.device, attr)._form_metadata
            
            forms.append({
                'command': metadata.command,
                'method': metadata.method,
                'params': metadata.params,
            })
            
        return forms
