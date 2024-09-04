

from typing import Dict, Any
from pydantic import BaseModel
from ochra_common.base import DataModel
from dataclasses import dataclass
from uuid import UUID


class ObjectCallRequest(BaseModel):
    method: str
    args: Dict | None = None


class ObjectCallResponse(BaseModel):
    return_data: Any
    status_code: int
    msg: str


class ObjectQueryResponse(BaseModel):
    id: UUID
    _cls: str


class ObjectPropertySetRequest(BaseModel):
    property: str
    property_value: Any


class ObjectConstructionRequest(BaseModel):
    object: BaseModel
