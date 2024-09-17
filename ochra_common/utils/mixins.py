from uuid import UUID
from ..connections.lab_connection import LabConnection


class RestProxyMixin:

    def _mixin_hook(self, endpoint: str, id: UUID) -> None:
        self._lab_conn = LabConnection()
        for field in self.model_fields.keys():

            def getter(self, name=field):
                return self._lab_conn.get_property(endpoint, id, name)

            def setter(self, value, name=field):
                print(f"set {name} to {value}")
                return self._lab_conn.set_property(endpoint, id, name, value)

            # Set the property on the class with the custom getter and setter
            setattr(self.__class__, field, property(getter, setter))

    def _lab_init(self, endpoint: str) -> None:
        self._lab_conn = LabConnection()
        self._lab_conn.construct_object(endpoint, self)


class RestProxyMixinReadOnly:

    def _mixin_hook(self, endpoint: str, name) -> None:
        id = self._lab_init(endpoint, name)
        for field in self.model_fields.keys():

            def getter(self, name=field):
                return self._lab_conn.get_property(endpoint, id, name)

            def setter(self, value, name=field):
                print("Read Only")

            # Set the property on the class with the custom getter and setter
            setattr(self.__class__, field, property(getter, setter))

    def _lab_init(self, endpoint: str, name: str) -> None:
        self._lab_conn: LabConnection = LabConnection()
        return self._lab_conn.get_object_by_name(endpoint, name).id
