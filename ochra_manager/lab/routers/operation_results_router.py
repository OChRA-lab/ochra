import logging
import uuid
from fastapi import APIRouter
from fastapi import HTTPException
from fastapi import File, UploadFile

# this is temp
from fastapi.responses import FileResponse, Response
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
COLLECTION = "operation_results"


class OperationResultRouter(APIRouter):
    def __init__(self, folderpath: str):
        prefix = f"/{COLLECTION}"
        super().__init__(prefix=prefix)
        self.lab_service = LabService(folderpath)
        self.put("/construct")(self.construct_result)
        self.get("/{object_id}/get_property/{property}")(self.get_property)
        self.patch("/{object_id}/modify_property")(self.modify_property)
        self.get("/get")(self.get_result)
        self.get("/{object_id}/get_data/")(self.get_data)
        self.patch("/{object_id}/put_data/")(self.put_data)

    async def construct_result(self, args: ObjectConstructionRequest):
        return self.lab_service.construct_object(args, COLLECTION)

    async def get_property(self, object_id: str, property: str):
        return self.lab_service.get_object_property(object_id, COLLECTION, property)

    async def modify_property(self, object_id: str, args: ObjectPropertySetRequest):
        return self.lab_service.patch_object(object_id, COLLECTION, args)

    async def get_result(self, identifier: str):
        if is_valid_uuid(identifier):
            value = self.lab_service.get_object_by_id(identifier, COLLECTION)
        else:
            value = self.lab_service.get_object_by_name(identifier, COLLECTION)
        return value

    async def get_data(self, object_id: str):
        value = self.lab_service.get_file(object_id, COLLECTION)
        response = Response(value)
        return response

    async def put_data(self, object_id: str, file: UploadFile = File(...)):
        result_data = await file.read()
        return self.lab_service.patch_file(object_id, COLLECTION, result_data)
