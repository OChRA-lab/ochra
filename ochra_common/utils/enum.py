from enum import IntEnum


class StationType(IntEnum):
    """
    An enumeration representing different types of stations.
    
    Attributes:
        STORAGE_STATION (int): Represents a storage station that does not have any devices (value: 0).
        WORK_STATION (int): Represents a work station (value: 1).
        MOBILE_ROBOT_STATION (int): Represents a mobile robot station (value: 2).
    """

    STORAGE_STATION = 0
    WORK_STATION = 1
    MOBILE_ROBOT_STATION = 2


class PhysicalState(IntEnum):
    """
    An enumeration representing different physical states of matter.
    
    Attributes:
        UNKNOWN (int): Represents an unknown physical state (value: -1).
        SOLID (int): Represents a solid state (value: 0).
        LIQUID (int): Represents a liquid state (value: 1).
        GAS (int): Represents a gas state (value: 2).
    """

    UNKNOWN = -1
    SOLID = 0
    LIQUID = 1
    GAS = 2


class ActivityStatus(IntEnum):
    """
    An enumeration representing different activity statuses for devices and stations.
    
    Attributes:
        ERROR (int): Represents an error state (value: -1).
        IDLE (int): Represents an idle state (value: 0).
        BUSY (int): Represents a busy state (value: 1).
    """

    ERROR = -1
    IDLE = 0
    BUSY = 1


class MobileRobotState(IntEnum):
    """
    An enumeration representing different states of a mobile robot.
    
    Attributes:
        ERROR (int): Represents an error state (value: -1).
        AVAILABLE (int): Robot is available for operation (value: 0).
        MANIPULATING (int): Robot is manipulating an object (value: 1).
        NAVIGATING (int): Robot is navigating through the environment (value: 2).
        CHARGING (int): Robot is charging its battery (value: 3).
    """

    ERROR = -1
    AVAILABLE = 0
    MANIPULATING = 1
    NAVIGATING = 2
    CHARGING = 3


class OperationStatus(IntEnum):
    """
    An enumeration representing different statuses of an operation.
    
    Attributes:
        CREATED (int): Operation has been created (value: 0).
        ASSIGNED (int): Operation has been assigned to a device or station (value: 1).
        IN_PROGRESS (int): Operation is currently in progress (value: 2).
        COMPLETED (int): Operation has been completed (value: 3).
    """

    CREATED = 0
    ASSIGNED = 1
    COMPLETED = 3
    IN_PROGRESS = 2


class ResultDataStatus(IntEnum):
    """
    An enumeration representing different statuses of result data.
    
    Attributes:
        UNAVAILABLE (int): Result data is unavailable yet(value: -1).
        UPLOADING (int): Result data is currently uploading (value: 0).
        AVAILABLE (int): Result data is available (value: 1).
    """

    UNAVAILABLE = -1
    UPLOADING = 0
    AVAILABLE = 1


class PatchType(IntEnum):
    """
    An enumeration representing different types of patches for modifying data structures.
    
    Attributes:
        SET (int): Represents a set operation (value: 1).
        LIST_APPEND (int): Represents an append operation for lists (value: 2).
        LIST_POP (int): Represents a pop operation for lists (value: 3).
        LIST_INSERT (int): Represents an insert operation for lists (value: 4).
        LIST_DELETE (int): Represents a delete operation for lists (value: 5).
        DICT_INSERT (int): Represents an insert operation for dictionaries (value: 6).
        DICT_DELETE (int): Represents a delete operation for dictionaries (value: 7).
    """

    SET = 1
    LIST_APPEND = 2
    LIST_POP = 3
    LIST_INSERT = 4
    LIST_DELETE = 5
    DICT_INSERT = 6
    DICT_DELETE = 7
