from dataclasses import dataclass
from ochra_common.agents.manipulator import Manipulator
from ochra_common.agents.mobile_platform import MobilePlatform


@dataclass
class MobileManipulator(Manipulator, MobilePlatform):
    pass
