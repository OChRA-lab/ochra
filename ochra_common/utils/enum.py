from enum import IntEnum


class StationType(IntEnum):
    """
    An enumeration representing different types of stations.
    """

    STORAGE_STATION = 0
    """Represents a storage station that does not have any devices"""

    WORK_STATION = 1
    """Represents a work station"""

    MOBILE_ROBOT_STATION = 2
    """Represents a mobile robot station"""


class PhysicalState(IntEnum):
    """
    An enumeration representing different physical states of matter.
    """

    UNKNOWN = -1
    """Represents an unknown physical state"""

    SOLID = 0
    """Represents a solid physical state"""

    LIQUID = 1
    """Represents a liquid physical state"""

    GAS = 2
    """Represents a gas physical state"""


class ActivityStatus(IntEnum):
    """
    An enumeration representing different activity statuses for devices and stations.
    """

    ERROR = -1
    """Represents an error state."""

    IDLE = 0
    """Represents an idle state."""

    BUSY = 1
    """Represents a busy state."""


class MobileRobotState(IntEnum):
    """
    An enumeration representing different states of a mobile robot.
    """

    ERROR = -1
    """Represents an error state."""

    AVAILABLE = 0
    """Robot is available for operation."""

    MANIPULATING = 1
    """Robot is manipulating an object."""

    NAVIGATING = 2
    """Robot is navigating through the environment."""

    CHARGING = 3
    """Robot is charging its battery."""


class OperationStatus(IntEnum):
    """
    An enumeration representing different statuses of an operation.
    """

    CREATED = 0
    """Operation has been created."""

    ASSIGNED = 1
    """Operation has been assigned to a device or station."""

    COMPLETED = 3
    """Operation has been completed."""

    IN_PROGRESS = 2
    """Operation is currently in progress."""


class ResultDataStatus(IntEnum):
    """
    An enumeration representing different statuses of result data.
    """

    UNAVAILABLE = -1
    """Result data is unavailable yet."""

    UPLOADING = 0
    """Result data is currently uploading."""

    AVAILABLE = 1
    """Result data is available."""


class PatchType(IntEnum):
    """
    An enumeration representing different types of patches for modifying data structures.
    """

    SET = 1
    """Represents a set operation."""

    LIST_APPEND = 2
    """Represents an append operation for lists."""

    LIST_POP = 3
    """Represents a pop operation for lists."""

    LIST_INSERT = 4
    """Represents an insert operation for lists."""

    LIST_DELETE = 5
    """Represents a delete operation for lists."""

    DICT_INSERT = 6
    """Represents an insert operation for dictionaries."""

    DICT_DELETE = 7
    """Represents a delete operation for dictionaries."""
