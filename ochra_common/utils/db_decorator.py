from dataclasses import fields
from OChRA_Common.ochra_common.connections.db_connection import DbConnection
from OChRA_Common.ochra_common.connections.lab_connection import LabConnection
from OChRA_Common.ochra_common.operations.operationModels import OperationDbModel


def backend_db(cls):
    """Decorator for replacing method calls for backend db interaction
    """

    def pre_init(self, **kwargs):
        self._db_conn = DbConnection()
        print("run pre init")

    def post_init(self, **kwargs):
        self.id = self._db_conn.create(
            self.collection_name, self)
        print("run post init")
        for field in fields(cls):
            # skip over id and collection_name
            if field.name == "id":
                continue
            if field.name == "collection_name":
                continue
            # Create custom getter

            def getter(self, name=field.name):
                value = self._db_conn.read(self.collection_name, self.id, name)
                print(f"Getting {name}: {value}")
                return value

            # Create custom setter
            def setter(self, value, name=field.name):
                print(self.id, self.collection_name)
                value = self._db_conn.update(
                    self.collection_name, self.id, {str(name): value})
                print(f"Setting {name} to: {value}")

            # Set the property on the class with the custom getter and setter
            setattr(cls, field.name, property(getter, setter))
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
        self.id = self._lab_conn.construct_object(
            cls, "operations",
            **kwargs
        )

    def post_init(self):
        # Loop through all fields defined in the dataclass
        for field in fields(cls):

            # Create custom getter
            def getter(self, name=field.name):
                value = self._db_conn.get(name)
                print(f"Getting {name}: {value}")
                return value

            # Create custom setter
            def setter(self, value, name=field.name):
                print(f"Setting {name} to {value} not allowed")

            # Set the property on the class with the custom getter and setter
            setattr(cls, field.name, property(getter, setter))

    orig_init = cls.__init__

    def new_init(self, *args, **kwargs):
        pre_init(self)
        orig_init(self, *args, **kwargs)
        post_init(self)

    cls.__init__ = new_init

    return cls
