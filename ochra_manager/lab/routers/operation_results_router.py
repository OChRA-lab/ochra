import logging
from os import remove
from fastapi import APIRouter, BackgroundTasks
from fastapi import File, UploadFile
from typing import Any

# this is temp
from fastapi.responses import FileResponse
from ochra_common.connections.api_models import (
    ObjectPropertyPatchRequest,
    ObjectConstructionRequest,
    ObjectPropertyGetRequest,
)
from ..lab_service import LabService
from ochra_common.base import DataModel
from ochra_common.utils.misc import is_valid_uuid, convert_to_data_model

COLLECTION = "operation_results"


class OperationResultRouter(APIRouter):
    """
    OperationResultRouter is responsible for handling operation result-related API endpoints.
    """

    def __init__(self, folderpath: str):
        prefix = f"/{COLLECTION}"
        super().__init__(prefix=prefix)
        self._logger = logging.getLogger(__name__)
        self.lab_service = LabService(folderpath)
        self.put("/")(self.construct_result)
        self.get("/{identifier}/property")(self.get_property)
        self.patch("/{identifier}/property")(self.modify_property)
        self.get("/")(self.get_result)
        self.get("/{identifier}/data/")(self.get_data)
        self.patch("/{identifier}/data/")(self.put_data)

    async def construct_result(self, args: ObjectConstructionRequest) -> str:
        """
        Construct a new operation result in the lab.

        Args:
            args (ObjectConstructionRequest): The construction parameters for the operation result.

        Returns:
            str: The ID of the constructed operation result.
        """
        self._logger.debug(f"Constructing operation result with args: {args}")
        return self.lab_service.construct_object(args, COLLECTION)

    async def get_property(
        self, identifier: str, args: ObjectPropertyGetRequest
    ) -> Any:
        """
        Get properties of an operation result.

        Args:
            identifier (str): The ID of the operation result.
            args (ObjectPropertyGetRequest): The properties to retrieve.

        Returns:
            Any: The requested properties of the operation result.
        """
        self._logger.debug(
            f"Getting property for operation result {identifier} with args: {args}"
        )
        return self.lab_service.get_object_property(identifier, COLLECTION, args)

    async def modify_property(
        self, identifier: str, args: ObjectPropertyPatchRequest
    ) -> bool:
        """
        Modify properties of an operation result.

        Args:
            identifier (str): The ID of the operation result.
            args (ObjectPropertyPatchRequest): The properties to modify.

        Returns:
            bool: True if the modification was successful, False otherwise.
        """
        self._logger.debug(
            f"Modifying property for operation result {identifier} with args: {args}"
        )
        return self.lab_service.patch_object(identifier, COLLECTION, args)

    async def get_result(self, identifier: str) -> DataModel:
        """
        Get an operation result by its ID.

        Args:
            identifier (str): The ID of the operation result.

        Returns:
            DataModel: The operation result data model.
        """
        if is_valid_uuid(identifier):
            result_obj = self.lab_service.get_object_by_id(identifier, COLLECTION)
        else:
            result_obj = self.lab_service.get_object_by_name(identifier, COLLECTION)
        self._logger.debug(f"Getting result for operation {identifier}")
        return convert_to_data_model(result_obj)

    async def get_data(
        self, identifier: str, background_tasks: BackgroundTasks
    ) -> FileResponse:
        """
        Get the data file associated with an operation result.

        Args:
            identifier (str): The ID of the operation result.
            background_tasks (BackgroundTasks): Background tasks for cleanup.

        Returns:
            FileResponse: The file response containing the data.
        """
        value, delete = self.lab_service.get_file(identifier, COLLECTION)
        response = FileResponse(value)
        if delete:
            background_tasks.add_task(remove, value)
        self._logger.debug(f"Getting data for operation result {identifier}")
        return response

    async def put_data(self, identifier: str, file: UploadFile = File(...)) -> None:
        """
        Upload and associate a data file with an operation result.
        
        Args:
            identifier (str): The ID of the operation result.
            file (UploadFile): The uploaded file.
        """
        result_data = await file.read()
        self._logger.debug(f"Putting data for operation result {identifier}")
        return self.lab_service.patch_file(identifier, COLLECTION, result_data)
