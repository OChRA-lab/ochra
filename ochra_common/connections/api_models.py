from typing import Dict, Any
from pydantic import BaseModel, Field
from uuid import UUID


class ObjectCallRequest(BaseModel):
    method: str
    args: Dict | None = None


class ObjectCallResponse(BaseModel):
    return_data: Any
    warnings: str = Field(default=None)


class ObjectQueryResponse(BaseModel):
    id: UUID
    cls: str


class ObjectPropertySetRequest(BaseModel):
    property: str
    property_value: Any


class ObjectConstructionRequest(BaseModel):
    object_json: str
