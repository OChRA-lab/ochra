import logging
from fastapi import APIRouter
from typing import Any, Dict
from ochra.common.connections.api_models import (
    ObjectCallRequest,
    ObjectPropertyPatchRequest,
    ObjectConstructionRequest,
    ObjectPropertyGetRequest,
)
from ..utils.lab_service import LabService
from ochra.common.base.data_model import DataModel
from ochra.common.utils.misc import is_valid_uuid, convert_to_data_model

COLLECTION = "devices"


class DeviceRouter(APIRouter):
    """
    DeviceRouter is responsible for handling device-related API endpoints.
    """

    def __init__(self, scheduler):
        prefix = f"/{COLLECTION}"
        super().__init__(prefix=prefix)
        self._logger = logging.getLogger(__name__)
        self.scheduler = scheduler
        self.lab_service = LabService()
        self.put("/")(self.construct_device)
        self.get("/{identifier}/property")(self.get_device_property)
        self.patch("/{identifier}/property")(self.modify_device_property)
        self.post("/{identifier}/method")(self.call_device)
        self.get("/")(self.get_device)
        self.delete("/{identifier}/")(self.delete_device)

    async def construct_device(self, args: ObjectConstructionRequest) -> str:
        """
        Construct a new device in the lab.

        Args:
            args (ObjectConstructionRequest): The construction parameters for the device.
        
        Returns:
            str: The ID of the constructed device.
        """
        # TODO: we need to assign the object to the station somehow
        self._logger.debug(f"Constructing device with args: {args}")
        return self.lab_service.construct_object(args, COLLECTION)

    async def get_device_property(
        self, identifier: str, args: ObjectPropertyGetRequest
    ) -> Any:
        """
        Get properties of a device.

        Args:
            identifier (str): The ID or name of the device.
            args (ObjectPropertyGetRequest): The properties to retrieve.

        Returns:
            Any: The requested properties of the device.
        """
        self._logger.debug(
            f"Getting property for device {identifier} with args: {args}"
        )
        return self.lab_service.get_object_property(identifier, COLLECTION, args)

    async def modify_device_property(
        self, identifier: str, args: ObjectPropertyPatchRequest
    ) -> bool:
        """
        Modify properties of a device.

        Args:
            identifier (str): The ID or name of the device.
            args (ObjectPropertyPatchRequest): The properties to modify.

        Returns:
            bool: True if the modification was successful, False otherwise.
        """
        self._logger.debug(
            f"Modifying property for device {identifier} with args: {args}"
        )
        return self.lab_service.patch_object(identifier, COLLECTION, args)

    async def call_device(
        self, identifier: str, args: ObjectCallRequest
    ) -> Dict[str, Any]:
        """
        Call a method on the device.

        Args:
            identifier (str): The ID or name of the device.
            args (ObjectCallRequest): The method call parameters.

        Returns:
            Dict[str, Any]: A dict representing the Operation model in JSON format.
        """
        op = self.lab_service.call_on_object(identifier, "device", args)
        self._logger.debug(f"Calling device {identifier} with args: {args}")
        self.scheduler.add_operation(op)
        return op.get_base_model().model_dump(mode="json")

    async def get_device(self, identifier: str) -> DataModel:
        """
        Get a device by its ID or name.

        Args:
            identifier (str): The ID or name of the device.

        Returns:
            DataModel: The device data model.
        """
        if is_valid_uuid(identifier):
            device_obj = self.lab_service.get_object_by_id(identifier, COLLECTION)
        else:
            device_obj = self.lab_service.get_object_by_name(identifier, COLLECTION)
        self._logger.debug(f"Getting device with identifier: {identifier}")
        return convert_to_data_model(device_obj)

    async def delete_device(self, identifier: str) -> Dict:
        """
        Delete a device by its ID or name.
        
        Args:
            identifier (str): The ID or name of the device.
        
        Returns:
            Dict: A message indicating the result of the deletion.
        """
        self._logger.debug(f"Deleting device with identifier: {identifier}")
        self.lab_service.delete_object(identifier, COLLECTION)
        return {"message": "Device deleted successfully"}
