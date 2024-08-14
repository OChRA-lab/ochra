from abc import abstractmethod
from dataclasses import dataclass
from ..base import DataModel
from typing import BinaryIO, Any


@dataclass
class OperationResult(DataModel):
    """Abstract result class to keep results formatted and structured"""
    type: str
    data: BinaryIO

    @abstractmethod
    def retrieve_processed_data() -> Any:
        pass
