

from typing import Dict
from pydantic import BaseModel


class ObjectSet(BaseModel):
    properties: Dict


class ObjectConstructionModel(BaseModel):
    catalogue_module: str
    object_type: str
    contstructor_params: Dict | None = None


class ObjectCallModel(BaseModel):
    object_function: str
    args: Dict | None = None
