from dataclasses import dataclass
from .manipulator import Manipulator
from .mobile_platform import MobilePlatform


@dataclass
class MobileManipulator(Manipulator, MobilePlatform):
    """Abstract manipulator robot that can move as well as execute tasks"""
    pass
