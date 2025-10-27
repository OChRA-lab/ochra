from ochra.common.storage.holder import Holder
from ochra.common.storage.container import Container
from ochra.common.utils.mixins import RestProxyMixin
from ochra.common.utils.enum import PatchType
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
            module_path="ochra.discovery.storage.holder",
        )
        self._mixin_hook(self._endpoint, self.id)

    def add_container(self, container: Type[Container]) -> None:
        """adds a container to the holders list of containers

        Args:
            container (Type[Container]): container to add
        """
        self._lab_conn.patch_property(self._endpoint, self.id, "containers", container, PatchType.LIST_APPEND)

    def remove_container(self, container: Type[Container]) -> None:
        """removes container from the holders list of containers

        Args:
            container (Type[Container]): container to remove
        """
        self._lab_conn.patch_property(self._endpoint, self.id, "containers", container, PatchType.LIST_DELETE)
