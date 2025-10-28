from .abstract import KukaKMRiiwaAbstract
from ochra.common.utils.mixins import RestProxyMixin
from ochra.common.equipment.device import HTMLForm, HTMLInput
import logging
from typing import Dict, Any, Annotated

logger = logging.getLogger(__name__)


class KukaKMRiiwa(KukaKMRiiwaAbstract, RestProxyMixin):
    def __init__(self, name, available_tasks):
        super().__init__(
            name=name,
            available_tasks=available_tasks,
            collection="robots",
            module_path="robots.kuka_kmriiwa.device",
        )
        self._mixin_hook("robots", self.id)

    @HTMLForm(call="execute", method="POST")
    def execute(
        self,
        task_name: Annotated[
            str, HTMLInput(label="Task Name", type="text", variable_binding="task_name")
        ],
        args: Annotated[
            Dict[str, Any],
            HTMLInput(label="Task Arguments", type="text", variable_binding="args"),
        ],
    ) -> bool:
        if task_name in self.available_tasks:
            logger.info(f"Executing task {task_name} with args {args}")
            return True
        else:
            logger.error(f"Task {task_name} not available")
            return False

    @HTMLForm(call="go_to", method="POST")
    def go_to(
        self,
        args: Annotated[
            Dict[str, Any],
            HTMLInput(label="Go To Arguments", type="text", variable_binding="args"),
        ],
    ) -> bool:
        logger.info(f"Navigating to new location using {args}")
        return True
