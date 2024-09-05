from uuid import UUID
from ..connections.lab_connection import LabConnection


class RestProxyMixin:

    def _mixin_hook(self, endpoint: str, id: UUID) -> None:
        for field in self.model_fields.keys():

            def getter(self, name=field):
                lab_conn: LabConnection = LabConnection()
                return lab_conn.get_property(endpoint, id, name)

            def setter(self, value, name=field):
                lab_conn: LabConnection = LabConnection()
                print(f"set {name} to {value}")
                return lab_conn.set_property(endpoint, id, name, value)

            # Set the property on the class with the custom getter and setter
            setattr(self.__class__, field, property(getter, setter))

    def _lab_init(self, endpoint: str) -> None:
        lab_conn: LabConnection = LabConnection()
        lab_conn.construct_object(endpoint, self)


class RestProxyMixinReadOnly:

    def _mixin_hook(self, endpoint: str, id: UUID) -> None:
        for field in self.model_fields.keys():

            def getter(self, name=field):
                lab_conn: LabConnection = LabConnection()
                return lab_conn.get_property(endpoint, id, name)

            def setter(self, value, name=field):
                return "Read Only"

            # Set the property on the class with the custom getter and setter
            setattr(self.__class__, field, property(getter, setter))

    def _lab_init(self, endpoint: str, name: str) -> None:
        lab_conn: LabConnection = LabConnection()
        lab_conn.get_object_by_name(endpoint, name)
