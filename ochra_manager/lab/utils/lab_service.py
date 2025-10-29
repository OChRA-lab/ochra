import logging
from typing import Any, List, Dict, Optional, Tuple

from ochra_common.equipment.operation import Operation
from fastapi import HTTPException
from ochra_common.connections.api_models import (
    ObjectCallRequest,
    ObjectPropertyPatchRequest,
    ObjectConstructionRequest,
    ObjectPropertyGetRequest,
)
from ...connections.db_connection import DbConnection
import json
from pathlib import Path
import shutil
from os import remove


class LabService:
    """
    LabService provides common functionality for managing laboratory objects and operations,
    abstracting database interactions and file management to avoid code duplication across routers.

    Attributes:
        db_conn (DbConnection): Database connection instance for CRUD operations.
        folderpath (Optional[Path]): Path to the folder for storing files, if provided.
    """

    def __init__(self, folderpath: Optional[str] = None) -> None:
        """
        Initialize the LabService with an optional folder path for file storage.

        Args:
            folderpath (Optional[str]): Path to the folder for storing files. If None, file operations are disabled.
        """
        self.db_conn: DbConnection = DbConnection()
        self._logger = logging.getLogger(__name__)

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
        """
        Update properties of an object in the specified collection.

        Args:
            object_id (str): Unique identifier of the object to update.
            collection (str): Name of the database collection containing the object.
            set_req (ObjectPropertyPatchRequest): Request containing the property name and new value.
            file (bool, optional): Indicates if the property being updated is a file. Defaults to False.

        Returns:
            bool: True if the update was successful.

        Raises:
            HTTPException: If the object does not exist or the update fails.
        """

        try:
            self.db_conn.read({"id": object_id, "_collection": collection})
            self._logger.debug(f"got Object {object_id}")
        except Exception as e:
            self._logger.debug(f"{object_id} does not exist")
            raise HTTPException(status_code=404, detail=str(e))
        try:
            self._logger.debug(
                f"attempting to update {set_req.property} to {set_req.property_value}"
            )  # noqa

            self.db_conn.update(
                {"id": object_id, "_collection": collection},
                set_req.model_dump(),
                file=file,
            )

            self._logger.debug(
                f"changed {set_req.property} to {set_req.property_value}"
            )

        except Exception as e:
            self._logger.error(e)
            raise HTTPException(status_code=500, detail=e)
        return True

    def construct_object(
        self, construct_req: ObjectConstructionRequest, collection: str
    ) -> str:
        """
        Create or update an object in the specified database collection.

        Args:
            construct_req (ObjectConstructionRequest): Request containing the object's JSON definition.
            collection (str): Name of the database collection.

        Returns:
            str: The ID of the constructed or updated object.

        Raises:
            HTTPException: If object creation or update fails.
        """

        object_dict: dict = json.loads(construct_req.object_json)
        existing_object = self.db_conn.find(
            {"_collection": collection}, {"name": object_dict.get("name", "")}
        )
        self._logger.info(f"existing_object: {existing_object}")
        if existing_object is not None:
            object_dict["id"] = existing_object.get("id")
            obj_inv = existing_object.get("inventory", None)
            if obj_inv is not None:
                object_dict["inventory"] = obj_inv
            self.db_conn.delete(
                {"id": existing_object.get("id"), "_collection": collection}
            )

        self.db_conn.create({"_collection": collection}, object_dict)
        self._logger.debug(f"constructed object of type {object_dict.get('cls')}")
        return object_dict.get("id")

    def call_on_object(
        self, object_id: str, object_type: str, call_req: ObjectCallRequest
    ) -> Operation:
        """
        Invoke a method on the specified object and record the operation.

        Args:
            object_id (str): ID of the target object.
            object_type (str): Type of the target object.
            call_req (ObjectCallRequest): Request containing method name, arguments, and caller information.

        Returns:
            Operation: The created Operation instance representing the method call.

        Raises:
            HTTPException: If the operation cannot be created or stored.
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
            self._logger.error(e)
            raise HTTPException(status_code=500, detail=str(e))

    def get_object_property(
        self, object_id: str, collection: str, request: ObjectPropertyGetRequest
    ) -> Any:
        """
        Retrieve a specific property value from an object in the given collection.

        Args:
            object_id (str): Unique identifier of the object.
            collection (str): Name of the database collection containing the object.
            request (ObjectPropertyGetRequest): Request specifying the property to retrieve.

        Returns:
            Any: The value of the requested property.

        Raises:
            HTTPException: If the object or property is not found.
        """
        try:
            return self.db_conn.read(
                {"id": object_id, "_collection": collection}, request.property
            )
        except Exception as e:
            raise HTTPException(status_code=404, detail=str(e))

    def get_object_by_name(self, name: str, collection: str) -> Dict[str, Any]:
        """
        Retrieve an object by its name from the specified collection.

        Args:
            name (str): The name of the object to retrieve.
            collection (str): The database collection containing the object.

        Returns:
            Dict[str, Any]: The object's JSON representation.

        Raises:
            HTTPException: If the object is not found.
        """
        try:
            return self.db_conn.find({"_collection": collection}, {"name": name})
        except Exception as e:
            raise HTTPException(status_code=404, detail=str(e))

    def get_object_by_id(self, object_id: str, collection: str) -> Dict[str, Any]:
        """
        Retrieve an object by its unique ID from the specified collection.

        Args:
            object_id (str): Unique identifier of the object to retrieve.
            collection (str): The database collection containing the object.

        Returns:
            Dict[str, Any]: The object's JSON representation.

        Raises:
            HTTPException: If the object is not found.
        """
        try:
            return self.db_conn.find({"_collection": collection}, {"id": object_id})
        except Exception as e:
            raise HTTPException(status_code=404, detail=str(e))

    def get_all_objects(
        self, collection: str, query_dict: Dict[str, Any] = None
    ) -> List[Dict[str, Any]]:
        """
        Retrieve all objects from the specified collection, optionally filtered by a query.

        Args:
            collection (str): Name of the database collection containing the objects.
            query_dict (Dict[str, Any], optional): Dictionary specifying query filters. Defaults to None.

        Returns:
            List[Dict[str, Any]]: List of objects represented as JSON dictionaries.

        Raises:
            HTTPException: If no objects are found or retrieval fails.
        """
        try:
            return self.db_conn.find_all({"_collection": collection}, query_dict)
        except Exception as e:
            raise HTTPException(status_code=404, detail=str(e))

    def patch_file(self, object_id: str, collection: str, result_data: bytes) -> None:
        """
        Update the file associated with an object in the database and manage its storage.

        Args:
            object_id (str): Unique identifier of the object to update.
            collection (str): Name of the database collection containing the object.
            result_data (bytes): Binary data to store as the file.
        """
        # self.db_conn.update(
        #     {"id": object_id, "_collection": collection},
        #     update={"result_data": result_data},
        #     file=True,
        # )
        parent_op = self.db_conn.find(
            {"_collection": "operations"}, {"result": object_id}
        )
        entity_id = self.db_conn.read(
            {"id": parent_op["id"], "_collection": "operations"}, property="entity_id"
        )
        entity_type = self.db_conn.read(
            {"id": parent_op["id"], "_collection": "operations"}, property="entity_type"
        )
        entity_name = self.db_conn.read(
            {"id": entity_id, "_collection": f"{entity_type}s"}, property="name"
        )
        if self.folderpath is not None:
            # create folder with the operation id
            path = self.folderpath / entity_name
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

    def get_file(self, object_id: str, collection: str) -> Tuple[Path, bool]:
        """
        Retrieve the file associated with an object from the database and local storage.

        Args:
            object_id (str): Unique identifier of the object whose file is to be retrieved.
            collection (str): Name of the database collection containing the object.

        Returns:
            Tuple[Path, bool]: The file path and a flag indicating if the file should be deleted after use.

        Raises:
            HTTPException: If the folder path is not set or the file cannot be found.
        """
        parent_op = self.db_conn.find(
            {"_collection": "operations"}, {"result": object_id}
        )
        entity_id = self.db_conn.read(
            {"id": parent_op["id"], "_collection": "operations"}, property="entity_id"
        )
        entity_type = self.db_conn.read(
            {"id": parent_op["id"], "_collection": "operations"}, property="entity_type"
        )
        entity_name = self.db_conn.read(
            {"id": entity_id, "_collection": f"{entity_type}s"}, property="name"
        )
        # TODO: zip up folder and delete for returns
        if self.folderpath is not None:
            delete = False
            # get the file path
            file_path: Path = (
                self.folderpath
                / entity_name
                / self.db_conn.read(
                    {"id": object_id, "_collection": collection},
                    property="data_file_name",
                )
            )
            if file_path.suffix == ".zip":
                # if the file is a directory, zip it up
                delete = True
                shutil.make_archive(str(file_path)[:-4], "zip", str(file_path)[:-4])
            return file_path, delete
        else:
            # if no folderpath is set, return None
            raise HTTPException(status_code=404, detail="Folder path not set")

    def delete_object(self, object_id: str, collection: str) -> None:
        """
        Delete an object from the specified database collection.

        Args:
            object_id (str): Unique identifier of the object to delete.
            collection (str): Name of the database collection containing the object.

        Raises:
            HTTPException: If the object is not found or deletion fails.
        """
        try:
            self.db_conn.delete({"id": object_id, "_collection": collection})
        except Exception as e:
            raise HTTPException(status_code=404, detail=str(e))
