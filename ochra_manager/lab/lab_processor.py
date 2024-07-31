
from datetime import datetime
import importlib
import logging
import pkgutil
from typing import Any
from ochra_common.connections.station_connection import StationConnection
from fastapi import HTTPException, Request
from bson import ObjectId
from bson.errors import InvalidId
from ochra_manager.lab.lab_request_models import ObjectSet, ObjectConstructionModel, ObjectCallModel
from mongoengine import ValidationError
from ochra_common.connections.db_connection import DbConnection

logger = logging.getLogger(__name__)


class LabProcessor():
    def __init__(self) -> None:
        self.objects_dict = {}
        self.db_conn: DbConnection = DbConnection(logger=logger)

    def _import_class_from_module(self, cls_name: str,
                                  module_path: str) -> Any:
        """import class from module

        Args:
            cls_name (str): class name
            module_path (str): path to module

        Returns:
            Any: None if error, otherwise attribute of given import
        """
        try:
            module = importlib.import_module(module_path)
            return getattr(module, cls_name, None)
        except (ModuleNotFoundError, ImportError):
            return None

    def _find_module_in_lib(self, cls_name, catalogue):
        """find module of a class in a given catalogue

        Args:
            cls_name (str): class name
            catalogue (str): catalogue to search

        Raises:
            NameError: if class is not found

        Returns:
            str: path to module
        """
        if catalogue not in ["robots", "devices", "containers", "reagents",
                             "operations"]:
            raise NameError(f"Catalogue {catalogue} is not defined")
        if catalogue == "operations":
            lib = "ochra_manager"
        elif catalogue == "robots":
            lib = "ochra_devices_front"
        elif catalogue == "devices":
            lib = "ochra_devices_front"
        pkg = importlib.import_module(f"{lib}.{catalogue}")
        for module_itr in pkgutil.iter_modules(
            path=pkg.__path__, prefix=f"{pkg.__name__}."
        ):
            module_path = f"{module_itr.name}"
            module = importlib.import_module(module_path)
            if hasattr(module, cls_name):
                return module_path
        raise NameError(f"Class type {cls_name} is not defined")

    def add_device(self, device):
        logger.info(f"added {device.object_id} to lab")
        self.objects_dict[str(device.object_id)] = device

    def create_station(self, request: Request):
        clientHost = request.client.host
        self.objects_dict[clientHost] = StationConnection(clientHost)
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

            obj = self.objects_dict[object_id]
            logger.debug(f"got Object {object_id}")
        except Exception as e:
            logger.info(f"{object_id} does not exist")
            raise HTTPException(status_code=404, detail=str(e))
        try:
            for arg in args.properties.keys():

                logger.debug(f"attempting {arg} to {arg.properties[arg]}")

                setattr(obj, arg, args.properties[arg])

                logger.info(f"changed {arg} to {args.properties[arg]}")

        except Exception as e:
            logger.error(e)
            raise HTTPException(status_code=500, detail=e)
        return object_id

    def construct_object(self, args: ObjectConstructionModel):
        """construct object of given type in db and instance

        Args:
            args (ObjectConstructionModel): Object construction model message

        Returns:
            str: object id of constructed object
        """
        string = "created object of type {} with params {} from category {}"
        string = string.format(args.object_type, args.contstructor_params,
                               args.catalogue_module)

        # placeholder for unimplemented catalogues
        if args.catalogue_module not in ["robots", "devices",
                                         "containers", "reagents",
                                         "operations"]:
            raise HTTPException(status_code=501, detail="Not implemented yet")
        else:
            try:
                if "Handler" in args.object_type:
                    logger.debug("removing handler tag")
                    args.object_type = args.object_type.replace("Handler", "")
                logstr = ("Trying to load module {} from {}")
                logger.debug(logstr.format(
                    args.object_type, args.catalogue_module))

                module = self._find_module_in_lib(
                    args.object_type, args.catalogue_module)
            # get backend class and construct
                logger.debug(f"attempting import of {args.object_type}")
                cls = self._import_class_from_module(
                    f"{args.object_type}", module)
                obj = cls(**args.contstructor_params)

            except ValidationError as e:

                logger.info(f"could not load {args.object_type}")
                raise HTTPException(status_code=500, detail=str(e))
            except TypeError as e:
                if "arguments" in str(e):
                    detail = str(e)
                else:
                    logger.debug(e)
                    detail = f"Type {args.object_type} does not \
                                exist on lab, {e}"
                logger.info(detail)
                raise HTTPException(
                    status_code=404, detail=detail)
            except Exception as e:
                logger.error(e)
                raise HTTPException(status_code=500, detail=str(e))
            # retrieve object_id and append to objects dict
            object_id = str(obj.db_data["id"])
            self.objects_dict[object_id] = obj
        logger.info(string)
        return object_id

    def call_on_object(self, object_id, call: ObjectCallModel):
        """call method of object on object

        Args:
            object_id (str): Object id of object to call on
            call (ObjectCallModel): object call model message

        Returns:
            str: object id of object post call
        """

        obj = self.objects_dict[object_id]

        method = getattr(obj, call.object_function)
        try:
            if "operation" in call.args:
                # get the op from the objects dict
                operation = self.objects_dict[call.args["operation"]]

                operation.status = "running"
                operation.start_timestamp = datetime.datetime.now()
                # attempt to run the operation
                result = method(operation.name, **operation.get_args())
                # update the operation status and end time
                operation.end_timestamp = datetime.datetime.now()
                operation.status = "completed"
                # if object id, add to results list
                objectid = ObjectId(result.data)
                # resultDoc = self.db_conn.read(
                #    OperationResultDbModel.collection_name, objectid)
                operation.add_data(objectid)
            else:
                result = method(**call.args)
        except (InvalidId, TypeError) as e:
            logger.warn(e)
        except Exception as e:
            operation.status = "failed"
            logger.error(e)
            raise HTTPException(status_code=500, detail=str(e))

        logger.info(f"called {call.object_function} on {obj.object_id}")

        return result

    def get_object(self, objectName):
        for object in self.objects_dict:
            if objectName == self.objects_dict[object].name:
                logger.info(f"got object {objectName}")
                return str(object)
        detail = f"could not find object with name {objectName}"
        logger.info(detail)
        raise HTTPException(status_code=404, detail=detail)
