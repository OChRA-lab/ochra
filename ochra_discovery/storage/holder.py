from ochra_common.storage.holder import Holder
from ochra_common.storage.container import Container
from ochra_common.utils.mixins import RestProxyMixin
from typing import Type


class Holder(Holder, RestProxyMixin):
    def __init__(self, type: str, max_capacity: int, capacity_unit: str):
        super().__init__(
            type=type,
            max_capacity=max_capacity,
            capacity_unit=capacity_unit,
            module_path="ochra_discovery.storage.vessel",
        )
        self._mixin_hook(self._endpoint, self.id)

    def add_container(self, container: Type[Container]) -> None:
        containers = self.containers
        containers.append(container)
        self.containers = containers

    def remove_container(self, container: Type[Container]) -> None:
        containers = self.containers
        containers.remove(container)
        self.containers = containers
