from ochra_common.operations.operationModels import Operation
from dataclasses import dataclass


@dataclass(kw_only=True)
class Dispense(Operation):
    volume: int
    material: str
    name: str = "Dispense"

    def basefoo(self):
        print("basefoo")
