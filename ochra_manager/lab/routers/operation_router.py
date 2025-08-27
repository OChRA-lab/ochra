import logging
from fastapi import APIRouter
from ochra_common.connections.api_models import (
    ObjectPropertyPatchRequest,
    ObjectConstructionRequest,
    ObjectPropertyGetRequest,
)
from ..lab_service import LabService
from ochra_common.utils.misc import is_valid_uuid, convert_to_data_model

COLLECTION = "operations"


class OperationRouter(APIRouter):
    def __init__(self):
        prefix = f"/{COLLECTION}"
        super().__init__(prefix=prefix)
        self._logger = logging.getLogger(__name__)
        self.lab_service = LabService()
        self.put("/")(self.construct_op)
        self.get("/{identifier}/property")(self.get_op_property)
        self.patch("/{identifier}/property")(self.modify_op_property)
        self.get("/")(self.get_op)

    async def construct_op(self, args: ObjectConstructionRequest):
        # TODO: we need to assign the object to the station somehow
        self._logger.debug(f"Constructing operation with args: {args}")
        return self.lab_service.construct_object(args, COLLECTION)

    async def get_op_property(self, identifier: str, args: ObjectPropertyGetRequest):
        self._logger.debug(f"Getting property for operation {identifier} with args: {args}")
        return self.lab_service.get_object_property(identifier, COLLECTION, args)

    async def modify_op_property(
        self, identifier: str, args: ObjectPropertyPatchRequest
    ):
        self._logger.debug(f"Modifying property for operation {identifier} with args: {args}")
        return self.lab_service.patch_object(identifier, COLLECTION, args)

    async def get_op(self, identifier: str):
        if is_valid_uuid(identifier):
            op_obj = self.lab_service.get_object_by_id(identifier, COLLECTION)
        else:
            op_obj = self.lab_service.get_object_by_name(identifier, COLLECTION)

        self._logger.debug(f"Getting operation with identifier: {identifier}")
        return convert_to_data_model(op_obj)
