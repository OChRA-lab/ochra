from .abstract import YuMiRobotAbstract
from ochra.common.utils.mixins import RestProxyMixinReadOnly
from typing import Dict, Any


class YuMiRobot(YuMiRobotAbstract, RestProxyMixinReadOnly):
    def __init__(self, name):
        super().__init__()
        self._mixin_hook(self._endpoint, name)

    def execute(self, task_name: str, args: Dict[str, Any]) -> bool:
        return self._lab_conn.call_on_object(
            self._endpoint, self.id, "execute", {"task_name": task_name, "args": args}
        )
