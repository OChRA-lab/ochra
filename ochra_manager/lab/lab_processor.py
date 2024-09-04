
from dataclasses import asdict
from datetime import datetime
import importlib
import logging
import pkgutil
from typing import Any
from ochra_common.connections.station_connection import StationConnection
from fastapi import HTTPException, Request
from bson import ObjectId
from bson.errors import InvalidId
from ochra_manager.lab.models.lab_api_models import ObjectCallRequest, ObjectPropertySetRequest
from ochra_manager.lab.models.lab_api_models import ObjectCallResponse, ObjectConstructionRequest
from ochra_manager.lab.models.operation import Operation
from ochra_manager.lab.models.DbObject import DbObject
from mongoengine import ValidationError
from ..connections.db_connection import DbConnection
import uuid


logger = logging.getLogger(__name__)


class lab_service():
    def __init__(self) -> None:
        self.db_conn: DbConnection = DbConnection()

    # @staticmethod
    # def add_device(device):
    #     logger.info(f"added {device.object_id} to lab")
    #     .objects_dict[str(device.object_id)] = device

    # @staticmethod
    # def create_station(request: Request):
    #     clientHost = request.client.host
    #     # TODO: create station objects here
    #     .objects_dict[clientHost] = StationConnection(clientHost + ":8000")
    #     return clientHost

    def patch_object(self, object_id, collection, args: ObjectPropertySetRequest):
        """patch properties of object_id using args key-value pairs

        Args:
            object_id (str): id of object to patch
            args (ObjectSet): key-value pairs of property to change
                                and value to change it to

        Returns:
            str: object id
        """

        try:
            self.db_conn.read({"id": object_id, "_collection": collection})
            logger.debug(f"got Object {object_id}")
        except Exception as e:
            logger.info(f"{object_id} does not exist")
            raise HTTPException(status_code=404, detail=str(e))
        try:

            logger.debug(f"attempting {args.property} to {args.property_value}")  # noqa

            self.db_conn.update({"id": object_id,
                                 "_collection": collection},
                                {args.property: args.property_value})

            logger.info(f"changed {args.property} to {args.property_value}")

        except Exception as e:
            logger.error(e)
            raise HTTPException(status_code=500, detail=e)
        return True

    def construct_object(self, args: ObjectConstructionRequest, collection):
        """construct object of given type in db and instance

        Args:
            args (ObjectConstructionRequest): Object construction model message

        Returns:
            str: object id of constructed object
        """

        string = "created object of type {}}"
        string = string.format(args.object._cls)
        id = self.db_conn.create({"_collection": collection}, args.object)
        return id

    def call_on_object(self, object_id, collection, call: ObjectCallRequest):
        """call method of object on object

        Args:
            object_id (str): Object id of object to call on
            call (ObjectCallModel): object call model message

        Returns:
            str: object id of object post call
        """

        try:
            # get station
            station_id = self.db_conn.read({"id": object_id, "_collection": collection},
                                           "station_id")

            station: StationConnection = StationConnection(station_id)
            # TODO create an operation object and save to db

            # call operation on station
            result = station.execute_op(
                call.method, self.db_conn.read({"id": object_id, "_collection": collection},
                                               "name"), **call.args)
            # return

        except (InvalidId, TypeError) as e:
            logger.warn(e)
        except Exception as e:
            # operation.status = "failed"
            logger.error(e)
            raise HTTPException(status_code=500, detail=str(e))

        logger.info(f"called {call.method} on {object_id}")

        return result

    def get_device(self, station_id, device_name):

        devices = self.db_conn.read(
            {"id": station_id, "_collection": "stations"}, "devices")
        for device_id in devices:
            device = self.db_conn.read(
                {"id": device_id, "_collection": "devices"}, "name")
            if device == device_name:
                return device_id
        raise HTTPException(status_code=404, detail="device not found")

    def get_object_property(self, id, collection, property):
        """Get property of object with id

        Args:
            id (str): id of object
            property (str): property of object to get

        Raises:
            HTTPException: if object not found or property not found

        Returns:
            Any: value of property
        """
        try:

            return self.db_conn.read({"id": id, "_collection": collection},
                                     property)
        except Exception as e:
            raise HTTPException(status_code=404, detail=str(e))

    def get_object_by_name(self, name, collection):
        # I DONT LIKE THIS I NEED TO COME UP WITH A BETTER SOLUTION

        return self.db_conn.read({"_collection": collection}, query={"name": name})
