from typing import Dict, Any
from pydantic import BaseModel, Field
from ..utils.enum import PatchType


class ObjectCallRequest(BaseModel):
    """
    Class that represents a request to call a method of an object.
    """

    method: str
    """The name of the method to be called."""

    caller_id: str
    """The unique identifier of the caller."""

    args: Dict | None = None
    """The arguments to be passed to the method. Defaults to None."""


class ObjectCallResponse(BaseModel):
    """
    Class that represents a response to an object method call.
    """

    return_data: Any
    """The data returned by the method call."""

    warnings: str = Field(default=None)
    """Any warnings generated during the method call. Defaults to None."""


class ObjectPropertyPatchRequest(BaseModel):
    """
    Class that represents a request to patch a property of an object.
    """

    property: str
    """The name of the property to be patched."""

    property_value: Any
    """The new value to be assigned to the property."""

    patch_type: PatchType = Field(default=PatchType.SET)
    """The type of patch to be applied. Defaults to PatchType.SET."""

    patch_args: Dict[str, Any] | None = Field(default=None)
    """Additional arguments for the patch operation. Defaults to None."""


class ObjectPropertyGetRequest(BaseModel):
    """
    Class that represents a request to get a property of an object.
    """

    property: str
    """The name of the property to be retrieved."""


class ObjectConstructionRequest(BaseModel):
    """
    Class that represents a request to construct a new object.
    """

    object_json: str
    """The JSON representation of the object to be constructed."""
