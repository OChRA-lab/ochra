from typing import Dict, Any, Optional
from pydantic import BaseModel, Field
from uuid import UUID
from typing import Union
from ..utils.enum import PatchType


class ObjectCallRequest(BaseModel):
    method: str
    caller_id: UUID
    args: Union[Dict, None] = None


class ObjectCallResponse(BaseModel):
    return_data: Any
    warnings: str = Field(default=None)


class ObjectPropertyPatchRequest(BaseModel):
    property: str
    property_value: Any
    patch_type: PatchType = Field(default=PatchType.SET)
    patch_args: Optional[Dict[str, Any]] = Field(default=None)


class ObjectPropertyGetRequest(BaseModel):
    property: str


class ObjectConstructionRequest(BaseModel):
    object_json: str
