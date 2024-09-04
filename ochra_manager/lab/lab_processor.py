
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
from ochra_common.connections.db_connection import DbConnection
import uuid


logger = logging.getLogger(__name__)


class lab_service():

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

    @staticmethod
    def patch_object(object_id, collection, args: ObjectPropertySetRequest):
        """patch properties of object_id using args key-value pairs

        Args:
            object_id (str): id of object to patch
            args (ObjectSet): key-value pairs of property to change
                                and value to change it to

        Returns:
            str: object id
        """
        db_conn: DbConnection = DbConnection()
        try:
            db_conn.read({"id": object_id, "_collection": collection})
            logger.debug(f"got Object {object_id}")
        except Exception as e:
            logger.info(f"{object_id} does not exist")
            raise HTTPException(status_code=404, detail=str(e))
        try:

            logger.debug(f"attempting {args.property} to {args.property_value}")

            db_conn.update({"id": object_id,
                            "_collection": collection},
                           {args.property: args.property_value})

            logger.info(f"changed {args.property} to {args.property_value}")

        except Exception as e:
            logger.error(e)
            raise HTTPException(status_code=500, detail=e)
        return True

    @staticmethod
    def construct_object(args: ObjectConstructionModel, collection):
        """construct object of given type in db and instance

        Args:
            args (ObjectConstructionModel): Object construction model message

        Returns:
            str: object id of constructed object
        """
        db_conn: DbConnection = DbConnection()
        string = "created object of type {} with params {}"
        string = string.format(args.object_type, args.contstructor_params)
        db_conn.create({"_collection": collection}, args.contstructor_params)
        return uuid.UUID(args.contstructor_params["id"])

    @staticmethod
    def call_on_object(object_id, collection, call: ObjectCallModel):
        """call method of object on object

        Args:
            object_id (str): Object id of object to call on
            call (ObjectCallModel): object call model message

        Returns:
            str: object id of object post call
        """
        db_conn: DbConnection = DbConnection()

        try:
            # get station
            station_id = db_conn.read({"id": object_id, "_collection": collection},
                                      "station_id")

            station: StationConnection = StationConnection(station_id)
            # TODO create an operation object and save to db

            # call operation on station
            result = station.execute_op(
                call.object_function, db_conn.read({"id": object_id, "_collection": collection},
                                                   "name"), **call.args)
            # return

        except (InvalidId, TypeError) as e:
            logger.warn(e)
        except Exception as e:
            # operation.status = "failed"
            logger.error(e)
            raise HTTPException(status_code=500, detail=str(e))

        logger.info(f"called {call.object_function} on {object_id}")

        return result

    @staticmethod
    def get_device(station_id, device_name):
        db_conn: DbConnection = DbConnection()
        devices = db_conn.read(
            {"id": station_id, "_collection": "stations"}, "devices")
        for device_id in devices:
            device = db_conn.read(
                {"id": device_id, "_collection": "devices"}, "name")
            if device == device_name:
                return device_id
        raise HTTPException(status_code=404, detail="device not found")

    @staticmethod
    def get_object_property(id, collection, property):
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
            db_conn: DbConnection = DbConnection()
            return db_conn.read({"id": id, "_collection": collection},
                                property)
        except Exception as e:
            raise HTTPException(status_code=404, detail=str(e))

    @staticmethod
    def get_object_by_name(name, collection):
        # TODO: implement this
        pass
