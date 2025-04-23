import logging
from typing import Any, List, Dict, Optional
from ..connections.station_connection import StationConnection
from ochra_common.equipment.operation import Operation
from fastapi import HTTPException
from ochra_common.connections.api_models import (
    ObjectCallRequest,
    ObjectPropertyPatchRequest,
    ObjectConstructionRequest,
    ObjectPropertyGetRequest,
)
from ochra_common.utils.misc import is_data_model, convert_to_data_model
from ..connections.db_connection import DbConnection
import json
from pathlib import Path
import shutil
from os import remove

logger = logging.getLogger(__name__)


class LabService:
    def __init__(self, folderpath: Optional[str] = None) -> None:
        """Labservice object serves the common functionality within routers to avoid code duplication
        """
        self.db_conn: DbConnection = DbConnection()

        # TODO: split this to check if the string is an actual directory to return some form of error message
        if folderpath and Path(folderpath).is_dir:
            self.folderpath = Path(folderpath)
            # make the actual folder in case it doesn't exist
            self.folderpath.mkdir(parents=True, exist_ok=True)
        else:
            self.folderpath = None

    def patch_object(
        self,
        object_id: str,
        collection: str,
        set_req: ObjectPropertyPatchRequest,
        file=False,
    ) -> bool:
        """patch properties of object_id using set_req key-value pairs

        Args:
            object_id (str): id of object to patch
            collection (str): db collection where the object will be stored
            set_req (ObjectPropertyPatchRequest): request for setting a property's value

        Returns:
            bool: True if successful

        Raises:
            HTTPException: if object not found or property not found
        """

        try:
            self.db_conn.read({"id": object_id, "_collection": collection})
            logger.debug(f"got Object {object_id}")
        except Exception as e:
            logger.info(f"{object_id} does not exist")
            raise HTTPException(status_code=404, detail=str(e))
        try:
            logger.debug(
                f"attempting to update {set_req.property} to {set_req.property_value}"
            )  # noqa
            
            self.db_conn.update(
                {"id": object_id, "_collection": collection},
                set_req.model_dump(),
                file=file,
            )

            logger.info(f"changed {set_req.property} to {set_req.property_value}")

        except Exception as e:
            logger.error(e)
            raise HTTPException(status_code=500, detail=e)
        return True

    def construct_object(
        self, construct_req: ObjectConstructionRequest, collection: str
    ) -> str:
        """construct object of given type in db and instance

        Args:
            construct_req (ObjectConstructionRequest): Object construction request
            collection (str): db collection where the object will be stored

        Returns:
            str: object id of constructed object
        """

        object_dict: dict = json.loads(construct_req.object_json)
        self.db_conn.create({"_collection": collection}, object_dict)
        logger.info(f"constructed object of type {object_dict.get('cls')}")
        return object_dict.get("id")

    def call_on_object(self, object_id: str, object_type: str, call_req: ObjectCallRequest) -> Operation:
        """call method of object on object

        Args:
            object_id (str): Object id of object to call on
            call_req (ObjectCallModel): object call model message

        Returns:
            Operation: Operation object representing the call
        """

        try:
            # create operation object and store in db
            op: Operation = Operation(
                entity_id=object_id,
                entity_type=object_type,
                caller_id=call_req.caller_id,
                method=call_req.method,
                args=call_req.args,
                collection="operations",
                module_path="ochra_discovery.equipment.operation",
            )

            # TODO change to use a proxy for operation instead of accessing db directly
            self.db_conn.create(
                {"_collection": "operations"}, json.loads(op.model_dump_json())
            )

            return op

        except HTTPException:
            raise

        except Exception as e:
            logger.error(e)
            raise HTTPException(status_code=500, detail=str(e))

    def get_object_property(
        self, object_id: str, collection: str, request: ObjectPropertyGetRequest
    ) -> Any:
        """Get property of object with id

        Args:
            object_id (str): id of object
            collection (str): db collection where the object will be stored
            property (str): property of object to get

        Raises:
            HTTPException: if object not found or property not found

        Returns:
            Any: value of property
        """
        try:
            return self.db_conn.read(
                {"id": object_id, "_collection": collection}, request.property
            )
        except Exception as e:
            raise HTTPException(status_code=404, detail=str(e))

    def get_object_by_name(self, name: str, collection: str) -> Dict[str, Any]:
        """Get object by name

        Args:
            name (str): name of object
            collection (str): db collection where the object will be stored

        Returns:
            str: object json representation

        Raises:
            HTTPException: if object not found
        """
        try:
            return self.db_conn.find(
                {"_collection": collection}, {"name": name}
            )
        except Exception as e:
            raise HTTPException(status_code=404, detail=str(e))

    def get_object_by_id(self, object_id: str, collection: str) -> Dict[str, Any]:
        """Get object by id

        Args:
            object_id (str): id of object
            collection (str): db collection where the object will be stored

        Returns:
            str: object json representation

        Raises:
            HTTPException: if object not found
        """
        try:
            return self.db_conn.find(
                {"_collection": collection}, {"id": object_id}
            )
        except Exception as e:
            raise HTTPException(status_code=404, detail=str(e))

    def get_all_objects(
        self, collection: str, query_dict: Dict[str, Any] = None
    ) -> List[Dict[str, Any]]:
        """Get all objects in collection

        Args:
            collection (str): db collection where the objects are stored

        Returns:
            List[str]: list of objects json representation

        Raises:
            HTTPException: if object not found
        """
        try:
            return self.db_conn.find_all(
                {"_collection": collection}, query_dict
            )
        except Exception as e:
            raise HTTPException(status_code=404, detail=str(e))

    def patch_file(self, object_id: str, collection: str, result_data):
        """update file in db

        Args:
            object_id (str): id to update
            collection (str): collection object is in
            result_data (bytestring): data to update it with
        """
        self.db_conn.update(
            {"id": object_id, "_collection": collection},
            update={"result_data": result_data},
            file=True,
        )

        if self.folderpath != None:
            # create folder with the operation id
            path = self.folderpath / object_id
            path.mkdir(exist_ok=True)

            # create the file within the folder
            filename = path / self.db_conn.read(
                {"id": object_id, "_collection": collection}, property="data_file_name"
            )
            with open(filename, "wb") as file:
                file.write(result_data)

            # unzip the file if the result data is a folder
            if (
                self.db_conn.read(
                    {"id": object_id, "_collection": collection}, property="data_type"
                )
                == "folder"
            ):
                shutil.unpack_archive(filename, filename.with_suffix(""), "zip")
                remove(filename)

    def get_file(self, object_id: str, collection: str):
        """get file from db

        Args:
            object_id (str): id of object to get
            collection (str): collection it is in

        Returns:
            bytestring: file data
        """
        return self.db_conn.read(
            {"id": object_id, "_collection": collection},
            property="result_data",
            file=True,
        )
