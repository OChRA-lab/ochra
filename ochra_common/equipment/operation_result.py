from abc import ABC, abstractmethod
from dataclasses import dataclass
from ochra_common.base import DataModel
from typing import BinaryIO, Any


@dataclass
class OperationResult(DataModel):
    type: str
    data: BinaryIO

    @abstractmethod
    def retrieve_processed_data() -> Any:
        pass
