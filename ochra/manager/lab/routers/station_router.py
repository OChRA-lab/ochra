import logging
from fastapi import APIRouter, Request
from typing import Any, Dict
from ochra.common.connections.api_models import (
    ObjectCallRequest,
    ObjectConstructionRequest,
    ObjectPropertyPatchRequest,
    ObjectPropertyGetRequest,
)
from ..utils.lab_service import LabService
from ochra.common.base.data_model import DataModel
from ochra.common.utils.misc import is_valid_uuid, convert_to_data_model
import json

COLLECTION = "stations"


class StationRouter(APIRouter):
    """
    StationRouter is responsible for handling station-related API endpoints.
    """

    def __init__(self, scheduler):
        super().__init__(prefix=f"/{COLLECTION}")
        self._logger = logging.getLogger(__name__)
        self.scheduler = scheduler
        self.lab_service = LabService()
        self.put("/")(self.construct_station)
        self.get("/{identifier}/property")(self.get_station_property)
        self.patch("/{identifier}/property")(self.modify_property)
        self.post("/{identifier}/method")(self.call_method)
        self.get("/")(self.get_station)
        self.delete("/{identifier}/")(self.delete_station)

    async def construct_station(
        self, args: ObjectConstructionRequest, request: Request
    ) -> str:
        """
        Construct a new station in the lab.

        Args:
            args (ObjectConstructionRequest): The construction parameters for the station.

        Returns:
            str: The ID of the constructed station.
        """
        self._logger.debug(f"Constructing station with args: {args}")
        object = json.loads(args.object_json)
        # TODO we can just set this as part of the station model
        object["station_ip"] = request.client.host
        args.object_json = json.dumps(object)
        return self.lab_service.construct_object(args, COLLECTION)

    async def get_station_property(
        self, identifier: str, args: ObjectPropertyGetRequest
    ) -> Any:
        """
        Get properties of a station.

        Args:
            identifier (str): The ID or name of the station.
            args (ObjectPropertyGetRequest): The properties to retrieve.

        Returns:
            Any: The requested properties of the station.
        """
        self._logger.debug(
            f"Getting property for station {identifier} with args: {args}"
        )
        return self.lab_service.get_object_property(identifier, COLLECTION, args)

    async def modify_property(
        self, identifier: str, args: ObjectPropertyPatchRequest
    ) -> bool:
        """
        Modify properties of a station.

        Args:
            identifier (str): The ID or name of the station.
            args (ObjectPropertyPatchRequest): The properties to modify.

        Returns:
            bool: True if the modification was successful, False otherwise.
        """
        self._logger.debug(
            f"Modifying property for station {identifier} with args: {args}"
        )
        return self.lab_service.patch_object(identifier, COLLECTION, args)

    async def call_method(
        self, identifier: str, args: ObjectCallRequest
    ) -> Dict[str, Any]:
        """
        Call a method on the station.

        Args:
            identifier (str): The ID or name of the station.
            args (ObjectCallRequest): The method call parameters.

        Returns:
            Dict[str, Any]: A dict representing the Operation model in JSON format.
        """
        op = self.lab_service.call_on_object(identifier, "station", args)
        self._logger.debug(f"Calling station {identifier} with args: {args}")
        self.scheduler.add_operation(op)
        return op.get_base_model().model_dump(mode="json")

    async def get_station(self, identifier: str) -> DataModel:
        """
        Get a station by its ID or name.

        Args:
            identifier (str): The ID or name of the station.

        Returns:
            DataModel: The station data model.
        """
        if is_valid_uuid(identifier):
            station_obj = self.lab_service.get_object_by_id(identifier, COLLECTION)
        else:
            station_obj = self.lab_service.get_object_by_name(identifier, COLLECTION)

        self._logger.debug(f"Getting station with identifier: {identifier}")
        return convert_to_data_model(station_obj)

    async def delete_station(self, identifier: str) -> Dict:
        """
        Delete a station by its ID or name.

        Args:
            identifier (str): The ID or name of the station.

        Returns:
            Dict: A message indicating the result of the deletion.
        """
        self._logger.debug(f"Deleting station with identifier: {identifier}")
        self.lab_service.delete_object(identifier, COLLECTION)
        return {"message": "Station deleted successfully"}
