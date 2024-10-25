import logging
from fastapi import APIRouter
from ochra_common.connections.api_models import (
    ObjectCallRequest,
    ObjectPropertySetRequest,
    ObjectConstructionRequest,
    ObjectQueryResponse,
)
from ..lab_service import LabService
from ochra_common.utils.misc import is_valid_uuid
from typing import Any

logger = logging.getLogger(__name__)
COLLECTION = "operations"


class OperationRouter(APIRouter):
    def __init__(self):
        prefix = f"/{COLLECTION}"
        super().__init__(prefix=prefix)
        self.lab_service = LabService()
        self.put("/construct")(self.construct_op)
        self.get("/{object_id}/get_property/{property}")(self.get_op_property)
        self.patch("/{object_id}/modify_property")(self.modify_op_property)
        self.get("/get")(self.get_op)

    async def construct_op(self, args: ObjectConstructionRequest):
        # TODO: we need to assign the object to the station somehow
        return self.lab_service.construct_object(args, COLLECTION)

    async def get_op_property(self, object_id: str, property: str):
        return self.lab_service.get_object_property(object_id, COLLECTION, property)

    async def modify_op_property(self, object_id: str, args: ObjectPropertySetRequest):
        return self.lab_service.patch_object(object_id, COLLECTION, args)

    async def get_op(self, identifier: str):
        if is_valid_uuid(identifier):
            return self.lab_service.get_object_by_id(identifier, COLLECTION)
        else:
            return self.lab_service.get_object_by_name(identifier, COLLECTION)

    async def get_data(self, identifier: str):
        return self.lab_service.get_data(identifier, COLLECTION)

    async def put_data(self, identifier: str, data: bytes):
        return self.lab_service.put_data(identifier, data, COLLECTION)