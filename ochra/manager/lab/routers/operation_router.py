import logging
from fastapi import APIRouter
from typing import Any
from ochra.common.connections.api_models import (
    ObjectPropertyPatchRequest,
    ObjectConstructionRequest,
    ObjectPropertyGetRequest,
)
from ..utils.lab_service import LabService
from ochra.common.base.data_model import DataModel
from ochra.common.utils.misc import is_valid_uuid, convert_to_data_model

COLLECTION = "operations"


class OperationRouter(APIRouter):
    """
    OperationRouter is responsible for handling operation-related API endpoints.
    """

    def __init__(self):
        prefix = f"/{COLLECTION}"
        super().__init__(prefix=prefix)
        self._logger = logging.getLogger(__name__)
        self.lab_service = LabService()
        self.put("/")(self.construct_op)
        self.get("/{identifier}/property")(self.get_op_property)
        self.patch("/{identifier}/property")(self.modify_op_property)
        self.get("/")(self.get_op)

    async def construct_op(self, args: ObjectConstructionRequest) -> str:
        """
        Construct a new operation in the lab.

        Args:
            args (ObjectConstructionRequest): The construction parameters for the operation.
        
        Returns:
            str: The ID of the constructed operation.
        """
        # TODO: we need to assign the object to the station somehow
        self._logger.debug(f"Constructing operation with args: {args}")
        return self.lab_service.construct_object(args, COLLECTION)

    async def get_op_property(self, identifier: str, args: ObjectPropertyGetRequest) -> Any:
        """
        Get properties of an operation.

        Args:
            identifier (str): The ID of the operation.
            args (ObjectPropertyGetRequest): The properties to retrieve.

        Returns:
            Any: The requested properties of the operation.
        """
        self._logger.debug(
            f"Getting property for operation {identifier} with args: {args}"
        )
        return self.lab_service.get_object_property(identifier, COLLECTION, args)

    async def modify_op_property(
        self, identifier: str, args: ObjectPropertyPatchRequest
    ) -> bool:
        """
        Modify properties of an operation.

        Args:
            identifier (str): The ID of the operation.
            args (ObjectPropertyPatchRequest): The properties to modify.

        Returns:
            bool: True if the modification was successful, False otherwise.
        """
        self._logger.debug(
            f"Modifying property for operation {identifier} with args: {args}"
        )
        return self.lab_service.patch_object(identifier, COLLECTION, args)

    async def get_op(self, identifier: str) -> DataModel:
        """
        Get an operation by its ID.

        Args:
            identifier (str): The ID of the operation.

        Returns:
            DataModel: The operation data model.
        """
        if is_valid_uuid(identifier):
            op_obj = self.lab_service.get_object_by_id(identifier, COLLECTION)
        else:
            op_obj = self.lab_service.get_object_by_name(identifier, COLLECTION)

        self._logger.debug(f"Getting operation with identifier: {identifier}")
        return convert_to_data_model(op_obj)
