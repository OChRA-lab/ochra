from dataclasses import fields
from ochra_common.connections.db_connection import DbConnection
from ochra_common.connections.lab_connection import LabConnection
from ochra_common.operations.operationModels import Operation


def backend_db(cls):
    """Decorator for replacing method calls for backend db interaction
    """

    def pre_init(self, **kwargs):
        self._db_conn = DbConnection()
        print("run pre init")

    def post_init(self, **kwargs):
        self.db_data["id"] = self._db_conn.create(self.db_data, self)
        print("run post init")
        for field in fields(self):
            # skip over db stuff
            if field.name in ["db_data"]:
                continue
            # Create custom getter

            def getter(self, name=field.name):
                value = self._db_conn.read(
                    self.db_data, name)
                print(f"Getting {name}: {value}")
                return value

            # Create custom setter
            def setter(self, value, name=field.name):
                value = self._db_conn.update(
                    self.db_data, {str(name): value})
                print(f"Setting {name} to: {value}")

            # Set the property on the class with the custom getter and setter
            setattr(cls, field.name, property(getter, setter))
            if field.name in kwargs:
                att = getattr(cls, field.name)
                att.fset(self, kwargs[field.name])

    original_init = cls.__init__

    def new_init(self, *args, **kwargs):
        pre_init(self, **kwargs)
        original_init(self, *args, **kwargs)
        post_init(self, **kwargs)

    cls.__init__ = new_init

    return cls


def frontend_db(cls):

    def pre_init(self, **kwargs):
        self._lab_conn = LabConnection()
        self._db_conn = DbConnection()

    def post_init(self, **kwargs):
        # Loop through all fields defined in the dataclass
        self.db_data["id"] = self._lab_conn.construct_object(
            cls, "operations",
            **kwargs
        )
        for field in fields(cls):
            # skip over db stuff
            if field.name in ["db_data"]:
                continue

            # Create custom getter
            def getter(self, name=field.name):
                value = self._db_conn.read(
                    self.db_data, name)
                print(f"Getting {name}: {value}")
                return value

            # Create custom setter
            def setter(self, value, name=field.name):
                raise AttributeError(
                    f"Attribute {name} is read-only")

            # Set the property on the class with the custom getter and setter
            setattr(cls, field.name, property(getter, setter))

    orig_init = cls.__init__

    def new_init(self, *args, **kwargs):
        pre_init(self, **kwargs)
        orig_init(self, *args, **kwargs)
        post_init(self, **kwargs)

    cls.__init__ = new_init

    return cls
