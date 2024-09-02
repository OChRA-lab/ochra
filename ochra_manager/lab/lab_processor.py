
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
from ochra_manager.lab.models.lab_request_models import ObjectSet, ObjectConstructionModel, ObjectCallModel
from ochra_manager.lab.models.operation import Operation
from ochra_manager.lab.models.DbObject import DbObject
from mongoengine import ValidationError
from ochra_common.connections.db_connection import DbConnection
import uuid


logger = logging.getLogger(__name__)


def add_device(self, device):
    logger.info(f"added {device.object_id} to lab")
    self.objects_dict[str(device.object_id)] = device


def create_station(self, request: Request):
    clientHost = request.client.host
    # TODO: create station objects here
    self.objects_dict[clientHost] = StationConnection(clientHost + ":8000")
    return clientHost


def patch_object(self, object_id, args: ObjectSet):
    """patch properties of object_id using args key-value pairs

    Args:
        object_id (str): id of object to patch
        args (ObjectSet): key-value pairs of property to change
                            and value to change it to

    Returns:
        str: object id
    """

    try:
        uuId = uuid.UUID(object_id)
        obj = self.objects_dict[uuId]
        logger.debug(f"got Object {object_id}")
    except Exception as e:
        logger.info(f"{object_id} does not exist")
        raise HTTPException(status_code=404, detail=str(e))
    try:
        for arg in args.properties.keys():

            logger.debug(f"attempting {arg} to {args.properties[arg]}")

            self.db_conn.update({"id": obj.id.hex,
                                 "_collection": obj._collection},
                                {arg: args.properties[arg]})

            logger.info(f"changed {arg} to {args.properties[arg]}")

    except Exception as e:
        logger.error(e)
        raise HTTPException(status_code=500, detail=e)
    return True


def construct_object(self, type, args: ObjectConstructionModel):
    """construct object of given type in db and instance

    Args:
        args (ObjectConstructionModel): Object construction model message

    Returns:
        str: object id of constructed object
    """
    string = "created object of type {} with params {}"
    string = string.format(args.object_type, args.contstructor_params)
    match(args.object_type):
        case "Device":
            device = DbObject()
            device._collection = type
            self.db_conn.create(device.db_data,
                                args.contstructor_params)
            device.id = uuid.UUID(args.contstructor_params["id"])
    # TODO add more cases for different object types/ remove match, unsure which we wanna go with
    self.objects_dict[device.id] = device
    return device.id


def call_on_object(self, object_id, call: ObjectCallModel):
    """call method of object on object

    Args:
        object_id (str): Object id of object to call on
        call (ObjectCallModel): object call model message

    Returns:
        str: object id of object post call
    """

    obj: DbObject = self.objects_dict[uuid.UUID(object_id)]
    try:
        # get station
        station: StationConnection = self.objects_dict[obj.get_property(
            "station_id")]
        # TODO create an operation object and save to db

        # call operation on station
        result = station.execute_op(
            call.object_function, obj.get_property("name"), **call.args)
        # return

    except (InvalidId, TypeError) as e:
        logger.warn(e)
    except Exception as e:
        # operation.status = "failed"
        logger.error(e)
        raise HTTPException(status_code=500, detail=str(e))

    logger.info(f"called {call.object_function} on {obj.id}")

    return result


def get_object(self, objectName):
    """Get object by name from the objects_dict

    Args:
        objectName (str): name of object to find

    Raises:
        HTTPException: if object not found

    Returns:
        str: objects id
    """
    for object in self.objects_dict:
        if hasattr(self.objects_dict[object], "get_property") and \
                objectName == self.objects_dict[object].get_property("name"):
            logger.info(f"got object {objectName}")
            return str(object)
    detail = f"could not find object with name {objectName}"
    logger.info(detail)
    raise HTTPException(status_code=404, detail=detail)


def get_object_property(self, id, property):
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
        uuId = uuid.UUID(id)
        obj = self.objects_dict[uuId]
        logger.debug(f"got Object {id}")
        return self.db_conn.read(obj.db_data,
                                 property)
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))
