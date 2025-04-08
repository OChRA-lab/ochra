import logging
import uuid
from fastapi import APIRouter
from fastapi import File, UploadFile

# this is temp
from fastapi.responses import FileResponse, Response
from ochra_common.connections.api_models import (
    ObjectPropertySetRequest,
    ObjectConstructionRequest,
    ObjectPropertyGetRequest
)
from ..lab_service import LabService
from ochra_common.utils.misc import is_valid_uuid, convert_to_data_model
from typing import Any

logger = logging.getLogger(__name__)
COLLECTION = "operation_results"


class OperationResultRouter(APIRouter):
    def __init__(self, folderpath: str):
        prefix = f"/{COLLECTION}"
        super().__init__(prefix=prefix)
        self.lab_service = LabService(folderpath)
        self.put("/construct")(self.construct_result)
        self.get("/{identifier}/get_property")(self.get_property)
        self.patch("/{identifier}/modify_property")(self.modify_property)
        self.get("/get")(self.get_result)
        self.get("/{identifier}/get_data/")(self.get_data)
        self.patch("/{identifier}/put_data/")(self.put_data)

    async def construct_result(self, args: ObjectConstructionRequest):
        return self.lab_service.construct_object(args, COLLECTION)

    async def get_property(self, identifier: str, args: ObjectPropertyGetRequest):
        return self.lab_service.get_object_property(identifier, COLLECTION, args)

    async def modify_property(self, identifier: str, args: ObjectPropertySetRequest):
        return self.lab_service.patch_object(identifier, COLLECTION, args)

    async def get_result(self, identifier: str):
        if is_valid_uuid(identifier):
            result_obj = self.lab_service.get_object_by_id(identifier, COLLECTION)
        else:
            result_obj = self.lab_service.get_object_by_name(identifier, COLLECTION)
        
        return convert_to_data_model(result_obj)

    async def get_data(self, identifier: str):
        value = self.lab_service.get_file(identifier, COLLECTION)
        response = Response(value)
        return response

    async def put_data(self, identifier: str, file: UploadFile = File(...)):
        result_data = await file.read()
        return self.lab_service.patch_file(identifier, COLLECTION, result_data)
