

from typing import Dict
from pydantic import BaseModel
from ochra_common.base import DataModel
from dataclasses import dataclass


class ObjectSet(BaseModel):
    properties: Dict


class ObjectConstructionModel(BaseModel):
    catalogue_module: str
    object_type: str
    contstructor_params: Dict | None = None


class ObjectCallModel(BaseModel):
    object_function: str
    args: Dict | None = None


@dataclass
class LabObject(DataModel):
    object_id: str
    object_type: str
    object_name: str
    station_id: str
