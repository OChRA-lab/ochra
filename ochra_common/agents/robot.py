from dataclasses import dataclass
from ochra_common.spaces.location import Location
from ochra_common.agents.agent import Agent


@dataclass
class Robot(Agent):
    type: str
    location: Location
