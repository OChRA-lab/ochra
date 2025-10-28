from .abstract import KukaKMRiiwaAbstract
from ochra.common.utils.mixins import RestProxyMixinReadOnly
from typing import Dict, Any


class KukaKMRiiwa(KukaKMRiiwaAbstract, RestProxyMixinReadOnly):
    def __init__(self, name):
        super().__init__()
        self._mixin_hook(self._endpoint, name)

    def execute(self, task_name: str, args: Dict[str, Any]) -> bool:
        return self._lab_conn.call_on_object(
            self._endpoint, self.id, "execute", {"task_name": task_name, "args": args}
        )

    def go_to(self, args: Dict[str, Any]) -> bool:
        return self._lab_conn.call_on_object(
            self._endpoint, self.id, method="go_to", args={"args": args}
        )
