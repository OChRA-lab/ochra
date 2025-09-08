import logging
from fastapi import APIRouter
from ..lab_service import LabService
from ochra_common.utils.misc import is_valid_uuid, convert_to_data_model

COLLECTIONS = ["stations", "robots", "scientists"]


class LabRouter(APIRouter):
    def __init__(self):
        prefix = "/lab"
        super().__init__(prefix=prefix)
        self._logger = logging.getLogger(__name__)
        self.lab_service = LabService()
        self.get("/{object_type}/get")(self.get_lab_object)
        self.get("/{object_type}/get_all")(self.get_lab_objects)

    async def get_lab_object(self, object_type: str, identifier: str):
        collection = object_type if object_type in COLLECTIONS else None
        if is_valid_uuid(identifier):
            lab_obj = self.lab_service.get_object_by_id(identifier, collection)
        else:
            lab_obj = self.lab_service.get_object_by_name(identifier, collection)
        self._logger.debug(f"Getting lab object with identifier: {identifier}")
        return convert_to_data_model(lab_obj)

    async def get_lab_objects(self, object_type: str):
        collection = object_type if object_type in COLLECTIONS else None
        lab_objs = self.lab_service.get_all_objects(collection)
        self._logger.debug(f"Getting all lab objects of type: {object_type}")
        return [convert_to_data_model(lab_obj) for lab_obj in lab_objs]
