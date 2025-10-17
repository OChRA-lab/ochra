from uuid import UUID
from typing import Any, Optional, Union
from copy import deepcopy
from pydantic import create_model
from ..connections.lab_connection import LabConnection
import inspect


class RestProxyMixin:
    """
    Mixin that changes class behavior such that its properties are accessed via REST API calls to a lab engine. This proxies both getters and setters.
    
    When used in a class, it replaces field getters and setters (except 'id' and 'cls') with property accessors that interact with the backend through
    LabConnection. This ensures property access is always synchronized with the remote data source.
    """

    _override_id = None

    # TODO remove object_id from the constructor
    def _mixin_hook(self, endpoint: str, object_id: UUID) -> None:
        """
        Initialize the mixin by setting up property accessors for model fields.
        
        Args:
            endpoint (str): The REST API endpoint for the model.
            object_id (UUID): The unique identifier for the model instance.
        """
        # add lab connection and construct object on the endpoint
        self._lab_conn = LabConnection()
        if self._override_id is None:
            self.id = self._lab_conn.construct_object(endpoint, self)
        else:
            self.id = self._override_id

        # change the getter and setter for each field to work with endpoint
        for field in self.model_fields.keys():
            if field not in ["id", "cls"]:

                def getter(self, name=field):
                    return self._lab_conn.get_property(endpoint, self.id, name)

                def setter(self, value, name=field):
                    return self._lab_conn.set_property(endpoint, self.id, name, value)

                # Set the property on the class with the custom getter and setter
                setattr(self.__class__, field, property(getter, setter))

    @classmethod
    def from_id(cls, object_id: UUID):
        """
        Create an instance of the class by fetching data from the REST API using the provided object ID.
        
        Args:
            object_id (UUID): The unique identifier for the model instance.
        
        Returns:
            An instance of the class populated with data from the REST API.
        """
        lab_conn: LabConnection = LabConnection()
        constructor_args = inspect.signature(cls)
        args = {}
        for arg in constructor_args.parameters:
            arg_value = lab_conn.get_property(
                cls._endpoint.default, str(object_id), arg
            )
            args[arg] = arg_value
        cls._override_id = object_id
        instance = cls(**args)
        instance.id = object_id
        cls._override_id = None
        return instance

    def _cleanup(self) -> None:
        """
        Clean up the data model instance by deleting it from the database.
        """
        lab: LabConnection = LabConnection()
        lab.delete_object(self._endpoint, self.id)


class RestProxyMixinReadOnly:
    """
    Mixin that changes class behavior such that its properties are accessed via REST API calls to a lab engine. This proxies only getters.
    
    When used in a class, it replaces field getters (except 'id' and 'cls') with property accessors that interact with the backend through
    LabConnection. This ensures property access is always synchronized with the remote data source.
    """

    def __new__(cls, *args, **kwargs):
        def make_field_optional(field, default: Any = None):
            new_field = deepcopy(field)
            new_field.default = default
            new_field.annotation = Optional[new_field.annotation]
            return new_field.annotation, new_field

        # create a new model with all optional fields to allow construction with no args
        fields = {
            field_name: make_field_optional(field_info)
            for field_name, field_info in cls.model_fields.items()
        }
        new_cls = create_model(
            cls.__name__, __base__=cls, __module__=cls.__module__, **fields
        )
        return super().__new__(new_cls)

    def _mixin_hook(self, endpoint: str, identifier: Union[str, UUID]) -> None:
        """
        Initialize the mixin by setting up property accessors for model fields.
        
        Args:
            endpoint (str): The REST API endpoint for the model.
            object_id (UUID): The unique identifier for the model instance.
        """
        self._lab_conn: LabConnection = LabConnection()

        # TODO add a check if the object is a device or something else
        if isinstance(identifier, UUID):
            self.id = identifier
        else:
            self.id = self._lab_conn.get_object_id(endpoint, identifier)
        self.cls = self._lab_conn.get_property(endpoint, self.id, "cls")

        # change the getter and setter for each field to work with endpoint
        for field_name in self.model_fields.keys():
            if field_name not in ["id", "cls"]:
                if (field_name == "result_data") and (
                    self._lab_conn.get_property(endpoint, self.id, "data_type")
                    in ["file", "folder"]
                ):

                    def getter(self, name=field_name):
                        return self._lab_conn.get_data("operation_results", self.id)

                else:

                    def getter(self, name=field_name):
                        return self._lab_conn.get_property(endpoint, self.id, name)

                def setter(self, value, name=field_name):
                    print("Read Only")

                # Set the property on the class with the custom getter and setter
                setattr(self.__class__, field_name, property(getter, setter))

    @classmethod
    def from_id(cls, object_id: UUID):
        """
        Create an instance of the class by fetching data from the REST API using the provided object ID.
        
        Args:
            object_id (UUID): The unique identifier for the model instance.
        
        Returns:
            An instance of the class populated with data from the REST API.
        """
        instance = cls.model_construct()
        instance._mixin_hook(cls._endpoint.default, object_id)
        return instance
