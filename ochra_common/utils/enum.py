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
    IN_PROGRESS = 2
    COMPLETED = 3

class ResultDataStatus(IntEnum):
    UNAVAILABLE = -1
    UPLOADING = 0
    AVAILABLE = 1
