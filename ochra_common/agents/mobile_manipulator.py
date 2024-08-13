from dataclasses import dataclass
from .manipulator import Manipulator
from .mobile_platform import MobilePlatform


@dataclass
class MobileManipulator(Manipulator, MobilePlatform):
    pass
