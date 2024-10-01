from uuid import UUID
from ..connections.lab_connection import LabConnection
import inspect


class RestProxyMixin:

    def _mixin_hook(self, endpoint: str, object_id: UUID) -> None:
        # add lab connection and construct object on the endpoint
        self._lab_conn = LabConnection()
        self._lab_conn.construct_object(
            endpoint + "/" + str(self.station_id), self)

        # change the getter and setter for each field to work with endpoint
        for field in self.model_fields.keys():
            if field not in ["id", "cls"]:
                def getter(self, name=field):
                    return self._lab_conn.get_property(endpoint, object_id, name)

                def setter(self, value, name=field):
                    print(f"set {name} to {value}")
                    return self._lab_conn.set_property(endpoint, object_id, name, value)

                # Set the property on the class with the custom getter and setter
                setattr(self.__class__, field, property(getter, setter))


class RestProxyMixinReadOnly:

    def _mixin_hook(self, endpoint: str, name) -> None:
        # add lab connection and get object id from the endpoint
        lab_conn = LabConnection()

        # TODO add a check if the object is a device or something else
        object_id = lab_conn.get_object(endpoint, name).id

        # change the getter and setter for each field to work with endpoint
        for field in self.model_fields.keys():
            if field not in ["id", "cls"]:
                def getter(self, name=field):
                    return lab_conn.get_property(endpoint, object_id, name)

                def setter(self, value, name=field):
                    print("Read Only")

                # Set the property on the class with the custom getter and setter
                setattr(self.__class__, field, property(getter, setter))

    @classmethod
    def from_id(cls, endpoint: str, object_id: UUID):
        lab_conn: LabConnection = LabConnection()
        constructer_args = inspect.signature(cls)
        args = {}
        for arg in constructer_args.parameters:
            arg_value = lab_conn.get_property(endpoint, object_id, arg)
            args[arg] = arg_value

        return cls(**args)
