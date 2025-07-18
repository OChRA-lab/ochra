import logging
from fastapi import APIRouter
from ochra_common.connections.api_models import (
    ObjectPropertyPatchRequest,
    ObjectConstructionRequest,
    ObjectPropertyGetRequest,
)
from ..lab_service import LabService
from ochra_common.utils.misc import is_valid_uuid, convert_to_data_model

logger = logging.getLogger(__name__)
COLLECTION = "operations"

class OperationRouter(APIRouter):
    def __init__(self):
        prefix = f"/{COLLECTION}"
        super().__init__(prefix=prefix)
        self.lab_service = LabService()
        self.put("/construct")(self.construct_op)
        self.get("/{identifier}/get_property")(self.get_op_property)
        self.patch("/{identifier}/modify_property")(self.modify_op_property)
        self.get("/get")(self.get_op)

    async def construct_op(self, args: ObjectConstructionRequest):
        # TODO: we need to assign the object to the station somehow
        return self.lab_service.construct_object(args, COLLECTION)

    async def get_op_property(self, identifier: str, args: ObjectPropertyGetRequest):
        return self.lab_service.get_object_property(identifier, COLLECTION, args)

    async def modify_op_property(self, identifier: str, args: ObjectPropertyPatchRequest):
        return self.lab_service.patch_object(identifier, COLLECTION, args)

    async def get_op(self, identifier: str):
        if is_valid_uuid(identifier):
            op_obj = self.lab_service.get_object_by_id(identifier, COLLECTION)
        else:
            op_obj = self.lab_service.get_object_by_name(identifier, COLLECTION)

        return convert_to_data_model(op_obj)
