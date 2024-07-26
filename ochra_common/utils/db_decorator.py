from dataclasses import fields
from ochra_common.connections.db_connection import DbConnection


def backend_db(cls):
    """Decorator for replacing method calls for backend db interaction 
    """

    def pre_init(self, **kwargs):
        self._db = DbConnection()

    original_init = cls.__init__

    def new_init(self, *args, **kwargs):
        pre_init(self, **kwargs)
        original_init(self, *args, **kwargs)

    cls.__init__ = new_init

    # Loop through all fields defined in the dataclass
    for field in fields(cls):

        # Create custom getter
        def getter(self, name=field.name):
            value = self._db.read(name)
            print(f"Getting {name}: {value}")
            return value

        # Create custom setter
        def setter(self, value, name=field.name):
            value = self._db.update(name, value)
            print(f"Setting {name} to: {value}")

        # Set the property on the class with the custom getter and setter
        setattr(cls, field.name, property(getter, setter))

    return cls


def frontend_db(cls):

    def pre_init(self):
        self._db = DbConnection()
        print("Pre init called")

    orig_init = cls.__init__

    def new_init(self, *args, **kwargs):
        pre_init(self)
        orig_init(self, *args, **kwargs)

    cls.__init__ = new_init

    # Loop through all fields defined in the dataclass
    for field in fields(cls):

        # Create custom getter
        def getter(self, name=field.name):
            value = self._db.get(name)
            print(f"Getting {name}: {value}")
            return value

        # Create custom setter
        def setter(self, value, name=field.name):
            print(f"Setting {name} to {value} not allowed")

        # Set the property on the class with the custom getter and setter
        setattr(cls, field.name, property(getter, setter))

    return cls
