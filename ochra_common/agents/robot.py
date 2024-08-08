from abc import ABC, abstractmethod
from dataclasses import dataclass
from ochra_common.base import DataModel
from ochra_common.spaces.location import Location
from ochra_common.agents.agent import Agent
from ochra_common.agents.robot_task import RobotTask


@dataclass
class Robot(DataModel, Agent, ABC):
    type: str
    location: Location
    
    @abstractmethod
    def execute(self, robot_task: RobotTask) -> bool:
        pass
    