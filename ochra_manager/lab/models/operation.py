from ochra_common.equipment.operation import Operation
from ochra_common.utils.db_decorator import backend_db


@backend_db
class Operation(Operation):
    pass
