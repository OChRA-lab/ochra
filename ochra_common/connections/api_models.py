from typing import Dict, Any
from pydantic import BaseModel, Field
from ..utils.enum import PatchType


class ObjectCallRequest(BaseModel):
    """
    Class that represents a request to call a method of an object.

    Attributes:
        method (str): The name of the method to be called.
        caller_id (str): The unique identifier of the caller.
        args (Dict | None): The arguments to be passed to the method. Defaults to None.
    """
    method: str
    caller_id: str
    args: Dict | None = None


class ObjectCallResponse(BaseModel):
    """
    Class that represents a response to an object method call.

    Attributes:
        return_data (Any): The data returned by the method call.
        warnings (str): Any warnings generated during the method call. Defaults to None.
    """
    return_data: Any
    warnings: str = Field(default=None)


class ObjectPropertyPatchRequest(BaseModel):
    """
    Class that represents a request to patch a property of an object.

    Attributes:
        property (str): The name of the property to be patched.
        property_value (Any): The new value to be assigned to the property.
        patch_type (PatchType): The type of patch to be applied. Defaults to PatchType.SET.
        patch_args (Dict[str, Any] | None): Additional arguments for the patch operation. Defaults to None.
    """
    property: str
    property_value: Any
    patch_type: PatchType = Field(default=PatchType.SET)
    patch_args: Dict[str, Any] | None = Field(default=None)


class ObjectPropertyGetRequest(BaseModel):
    """
    Class that represents a request to get a property of an object.

    Attributes:
        property (str): The name of the property to be retrieved.
    """
    property: str


class ObjectConstructionRequest(BaseModel):
    """
    Class that represents a request to construct a new object.

    Attributes:
        object_json (str): The JSON representation of the object to be constructed.
    """
    object_json: str
