from ochra_common.storage.holder import Holder
from ochra_common.storage.container import Container
from ochra_common.utils.mixins import RestProxyMixin
from typing import Type


class Holder(Holder, RestProxyMixin):
    def __init__(self, type: str, max_capacity: int):
        """Holder object is a container that can hold other containers

        Args:
            type (str): type of holder
            max_capacity (int): Max capacity of the holder
        """
        super().__init__(
            type=type,
            max_capacity=max_capacity,
            collection="containers",
            module_path="ochra_discovery.storage.holder",
        )
        self._mixin_hook(self._endpoint, self.id)

    def add_container(self, container: Type[Container]) -> None:
        """adds a container to the holders list of containers

        Args:
            container (Type[Container]): container to add
        """
        containers = self.containers
        containers.append(container)
        self.containers = containers

    def remove_container(self, container: Type[Container]) -> None:
        """removes container from the holders list of containers

        Args:
            container (Type[Container]): container to remove
        """
        containers = self.containers
        containers.remove(container)
        self.containers = containers
