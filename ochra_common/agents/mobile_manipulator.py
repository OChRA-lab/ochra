from .manipulator import Manipulator
from .mobile_platform import MobilePlatform


class MobileManipulator(Manipulator, MobilePlatform):
    """
    Abstract manipulator robot that can move as well as execute tasks.

    This class combines the functionalities of both a manipulator and a mobile platform.
    """

    pass
