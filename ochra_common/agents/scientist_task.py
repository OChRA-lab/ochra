from dataclasses import dataclass
from .task import Task


@dataclass
class ScientistTask(Task):
    """Abstract task specifically for scientists"""
    pass
