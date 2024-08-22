from ochra_common.equipment.device import Device as AbstractDevice
from ochra_common.utils.db_decorator import middle_db


@middle_db
class Device(AbstractDevice):
    def __init__(self, **kwargs):
        super().__init__(
            name=kwargs["name"],
            status=kwargs["status"],
            _cls=kwargs["_cls"],
            _collection=kwargs["_collection"],
            inventory=kwargs["inventory"],
            operation_history=kwargs["operation_history"],
            station_id=kwargs.get("station_id", None))
