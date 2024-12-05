import logging
from typing import Any, List, Dict
from ..connections.station_connection import StationConnection
from ochra_common.equipment.operation import Operation
from fastapi import HTTPException
from ochra_common.connections.api_models import (
    ObjectCallRequest,
    ObjectPropertySetRequest,
    ObjectConstructionRequest,
)
from ..connections.db_connection import DbConnection
import uuid
import json
from datetime import datetime

logger = logging.getLogger(__name__)


class LabService:
    def __init__(self) -> None:
        self.db_conn: DbConnection = DbConnection()

    def patch_object(
        self,
        object_id: str,
        collection: str,
        set_req: ObjectPropertySetRequest,
        file=False,
    ) -> bool:
        """patch properties of object_id using set_req key-value pairs

        Args:
            object_id (str): id of object to patch
            collection (str): db collection where the object will be stored
            set_req (ObjectPropertySetRequest): request for setting a property's value

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
                {set_req.property: set_req.property_value},
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

    def call_on_object(
        self, object_id: str, collection: str, call_req: ObjectCallRequest
    ) -> str:
        """call method of object on object

        Args:
            object_id (str): Object id of object to call on
            collection (str): db collection where the object will be stored
            call_req (ObjectCallModel): object call model message

        Returns:
            str: object id of object post call
        """

        try:
            if collection == "devices" or collection == "robots":
                # get station ip
                station_id = self.db_conn.read(
                    {"id": object_id, "_collection": collection}, "station_id"
                )

                if station_id is None:
                    raise HTTPException(status_code=404, detail="station not found")

                station_ip = self.db_conn.read(
                    {"id": station_id, "_collection": "stations"}, "station_ip"
                )
                
                station_port = self.db_conn.read(
                    {"id": station_id, "_collection": "stations"}, "port"
                )
                # create station connection
                station_client: StationConnection = StationConnection(
                    station_ip + ":" +str(station_port)
                )

                # create operation object and store in db
                op: Operation = Operation(
                    caller_id=object_id,
                    method=call_req.method,
                    args=call_req.args,
                    module_path="ochra_discovery.equipment.operation",
                )
                # TODO change to use a proxy for operation instead of accessing db directly
                self.db_conn.create(
                    {"_collection": "operations"}, json.loads(op.model_dump_json())
                )

                # pass operation to station to execute
                is_robot_op = collection == "robots"
                result = station_client.execute_op(op, is_robot_op=is_robot_op)

                # TODO change to use a proxy for operation instead of accessing db directly
                self.db_conn.update(
                    {"id": object_id, "_collection": "operations"},
                    {"result": result.data},
                )

                logger.info(f"called {call_req.method} on {object_id}")

                # TODO change later to return a better response
                return op.model_dump(mode="json")

            elif collection == "stations":
                # TODO do station stuff
                pass

        except HTTPException:
            raise

        except Exception as e:
            logger.error(e)
            raise HTTPException(status_code=500, detail=str(e))

    def get_object_property(
        self, object_id: str, collection: str, property: str
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
                {"id": object_id, "_collection": collection}, property
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
            return self.db_conn.find({"_collection": collection}, {"name": name})
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
            return self.db_conn.find({"_collection": collection}, {"id": object_id})
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
            return self.db_conn.find_all({"_collection": collection}, query_dict)
        except Exception as e:
            raise HTTPException(status_code=404, detail=str(e))

    def get_object_by_station_and_type(
        self, station_identifier: str, collection: str, obj_type: str
    ) -> str:
        """Get object by station and type

        Args:
            station_identifier (str): station id or name
            collection (str): db collection where the object will be stored
            obj_type (str): object type

        Returns:
            str: object json representation

        Raises:
            HTTPException: if object not found
        """
        try:
            uuid.UUID(station_identifier)
            return self.db_conn.find(
                {"_collection": collection},
                {"station_id": station_identifier, "_cls": obj_type},
            )
        except ValueError:
            station_id = self.db_conn.find(
                {"_collection": "stations"}, {"name": station_identifier}
            )
            return self.db_conn.find(
                {"_collection": collection},
                {"station_id": station_id, "_cls": obj_type},
            )
        except Exception as e:
            raise HTTPException(status_code=404, detail=str(e))

    def patch_file(self, object_id: str, collection: str, result_data):
        self.db_conn.update(
            {"id": object_id, "_collection": collection},
            update={"result_data": result_data},
            file=True,
        )

    def get_file(self, object_id: str, collection: str):
        return self.db_conn.read(
            {"id": object_id, "_collection": collection}, property="result_data", file=True
        )
