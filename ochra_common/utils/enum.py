from enum import IntEnum


class StationType(IntEnum):
    STORAGE_STATION = 0
    WORK_STATION = 1
    MOBILE_ROBOT_STATION = 2


class PhysicalState(IntEnum):
    UNKNOWN = -1
    SOLID = 0
    LIQUID = 1
    GAS = 2


class ActivityStatus(IntEnum):
    ERROR = -1
    IDLE = 0
    BUSY = 1


class MobileRobotState(IntEnum):
    ERROR = -1
    AVAILABLE = 0
    MANIPULATING = 1
    NAVIGATING = 2
    CHARGING = 3


class OperationStatus(IntEnum):
    CREATED = 0
    ASSIGNED = 1
    COMPLETED = 3
    IN_PROGRESS = 2


class ResultDataStatus(IntEnum):
    UNAVAILABLE = -1
    UPLOADING = 0
    AVAILABLE = 1


class PatchType(IntEnum):
    SET = 1 # "set"
    LIST_APPEND = 2 # "list.append"
    LIST_POP = 3 # "list.pop"
    LIST_INSERT = 4 # "list.insert"
    LIST_DELETE = 5 # "list.delete"
    DICT_INSERT = 6 # "dict.insert"
    DICT_DELETE = 7 # "dict.delete"
