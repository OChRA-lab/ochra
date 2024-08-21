from dataclasses import fields
from typing import Any
from OChRA_Common.ochra_common.connections.db_connection import DbConnection
from OChRA_Common.ochra_common.connections.lab_connection import LabConnection
from ochra_common.operations.operationModels import Operation
from ochra_common.equipment.device import Device
from dataclasses import asdict
from ochra_common.utils.singleton_meta import SingletonMeta
import uuid


class Offline(metaclass=SingletonMeta):
    def __init__(self, offline=False):
        self.offline = offline

    def __call__(self, *args: Any, **kwds: Any) -> Any:
        return self.offline


def middle_db(cls):
    """Decorator for replacing method calls for backend db interaction
    """

    def pre_init(self, **kwargs):
        self._db_conn = DbConnection()
        print("run pre init")

    def post_init(self, **kwargs):
        self._db_conn.create(self.to_dict(), kwargs)
        print("run post init")
        for field in fields(self):
            # skip over db stuff
            if field.name in ["id"]:
                continue
            if field.name.startswith("_"):
                continue
            # Create custom getter

            def getter(self, name=field.name):
                value = self._db_conn.read(
                    {"id": self.id.hex,
                     "_cls": self._cls,
                     "_collection": self._collection}, name)
                print(f"Getting {name}: {value}")
                return value

            # Create custom setter
            def setter(self, value, name=field.name):
                value = self._db_conn.update(
                    {"id": self.id.hex,
                     "_cls": self._cls,
                     "_collection": self._collection}, {str(name): value})
                print(f"Setting {name} to: {value}")

            # Set the property on the class with the custom getter and setter
            setattr(cls, field.name, property(getter, setter))
            # if field.name in kwargs:
            #    att = getattr(cls, field.name)
            #    att.fset(self, kwargs[field.name])

    original_init = cls.__init__

    def new_init(self, *args, **kwargs):
        pre_init(self, **kwargs)
        original_init(self, *args, **kwargs)
        post_init(self, **kwargs)

    cls.__init__ = new_init

    return cls


def frontend_db(isDevice=False):
    def decorator(cls):

        def pre_init(self, **kwargs):
            self._lab_conn = LabConnection()
            self._db_conn = DbConnection()

        def post_init(self, **kwargs):
            # Loop through all fields defined in the dataclass
            if isDevice:
                self.id = uuid.UUID(self._lab_conn.get_object(
                    self.name))
            else:
                self._lab_conn.construct_object(
                    self.__class__, "Devices",
                    **self.to_dict()
                )
            for field in fields(cls):
                # skip over db stuff
                if field.name in ["id", "db_data"]:
                    continue
                if field.name.startswith("_"):
                    continue
                if field.metadata.get("backend_only"):
                    continue

                # Create custom getter
                def getter(self, name=field.name):
                    value = self._db_conn.read(
                        {"id": self.id.hex,
                         "_cls": self._cls,
                         "_collection": self._collection}, name)
                    print(f"Getting {name}: {value}")
                    return value

                # Create custom setter
                def setter(self, value, name=field.name):
                    print(f"Attribute {name} is read-only")

                # Set the property on the class with the custom getter and setter
                setattr(cls, field.name, property(getter, setter))

            for func in cls.__dict__:
                if callable(cls.__dict__[func]):
                    if not hasattr(func, "change"):
                        setattr(cls, func, frontend_function(
                            cls.__dict__[func]))

        orig_init = cls.__init__

        def new_init(self, *args, **kwargs):
            pre_init(self, **kwargs)
            orig_init(self, *args, **kwargs)
            post_init(self, **kwargs)

        cls.__init__ = new_init

        return cls
    return decorator


def frontend_function(func):
    def wrapper(self, **kwargs):
        lab_conn: LabConnection = LabConnection()
        result = lab_conn.call_on_object(self.id, func.__name__, **kwargs)
        return result
    return wrapper


def frontend_function_to_ignore(func):
    def wrapper(*args, **kwargs):
        setattr(func, "change", False)
        result = func(*args, **kwargs)
        return result
    return wrapper


def backend_db(cls):
    def pre_init(self, **kwargs):
        self._lab_conn = LabConnection()
        print("run pre init")

    def post_init(self, **kwargs):
        if issubclass(cls, Device):
            self._lab_conn.construct_object(
                Device, "Devices",
                **self.to_dict()
            )
        print("run post init")
        for field in fields(self):
            # skip over db stuff
            if field.name in ["id"]:
                continue
            if field.name.startswith("_"):
                continue
            # Create custom getter

            def getter(self, name=field.name):
                value = self._lab_conn.get_property(
                    self.id.hex, name)
                print(f"Getting {name}: {value}")
                return value

            # Create custom setter
            def setter(self, value, name=field.name):
                value2 = self._lab_conn.patch_object(
                    self.id.hex, **{str(name): value})
                print(f"Setting {name} to: {value2}")

            # Set the property on the class with the custom getter and setter
            setattr(cls, field.name, property(getter, setter))
            # if field.name in kwargs:
            #    att = getattr(cls, field.name)
            #    att.fset(self, kwargs[field.name])

    original_init = cls.__init__

    def new_init(self, *args, **kwargs):
        offline = Offline()
        if offline.offline:
            original_init(self,*args,**kwargs)
        else:
            pre_init(self, **kwargs)
            original_init(self, *args, **kwargs)
            post_init(self, **kwargs)

    cls.__init__ = new_init

    return cls
