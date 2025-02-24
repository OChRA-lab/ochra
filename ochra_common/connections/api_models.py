from typing import Dict, Any
from pydantic import BaseModel, Field
from uuid import UUID
from typing import Union


class ObjectCallRequest(BaseModel):
    method: str
    caller_id: UUID
    args: Union[Dict, None] = None


class ObjectCallResponse(BaseModel):
    return_data: Any
    warnings: str = Field(default=None)


class ObjectQueryResponse(BaseModel):
    id: UUID
    cls: str
    module_path: str


class ObjectPropertySetRequest(BaseModel):
    property: str
    property_value: Any


class ObjectPropertyGetRequest(BaseModel):
    property: str


class ObjectConstructionRequest(BaseModel):
    object_json: str
