import logging
from fastapi import APIRouter
from typing import Any, Dict
from ochra_common.connections.api_models import (
    ObjectCallRequest,
    ObjectPropertyPatchRequest,
    ObjectConstructionRequest,
    ObjectPropertyGetRequest,
)
from ..lab_service import LabService
from ochra_common.base import DataModel
from ochra_common.utils.misc import is_valid_uuid, convert_to_data_model

COLLECTION = "robots"


class RobotRouter(APIRouter):
    """
    RobotRouter is responsible for handling robot-related API endpoints.
    """

    def __init__(self, scheduler):
        prefix = f"/{COLLECTION}"
        super().__init__(prefix=prefix)
        self._logger = logging.getLogger(__name__)
        self.scheduler = scheduler
        self.lab_service = LabService()
        self.put("/")(self.construct_robot)
        self.get("/{identifier}/property")(self.get_property)
        self.patch("/{identifier}/property")(self.modify_property)
        self.post("/{identifier}/method")(self.call_robot)
        self.get("/")(self.get_robot)
        self.delete("/{identifier}/")(self.delete_robot)

    async def construct_robot(self, args: ObjectConstructionRequest) -> str:
        """
        Construct a new robot in the lab.

        Args:
            args (ObjectConstructionRequest): The construction parameters for the robot.

        Returns:
            str: The ID of the constructed robot.
        """
        self._logger.debug(f"Constructing robot with args: {args}")
        return self.lab_service.construct_object(args, COLLECTION)

    async def get_property(
        self, identifier: str, args: ObjectPropertyGetRequest
    ) -> Any:
        """
        Get properties of a robot.

        Args:
            identifier (str): The ID or name of the robot.
            args (ObjectPropertyGetRequest): The properties to retrieve.

        Returns:
            Any: The requested properties of the robot.
        """
        self._logger.debug(f"Getting property for robot {identifier} with args: {args}")
        return self.lab_service.get_object_property(identifier, COLLECTION, args)

    async def modify_property(
        self, identifier: str, args: ObjectPropertyPatchRequest
    ) -> bool:
        """
        Modify properties of a robot.

        Args:
            identifier (str): The ID or name of the robot.
            args (ObjectPropertyPatchRequest): The properties to modify.

        Returns:
            bool: True if the modification was successful, False otherwise.
        """
        self._logger.debug(
            f"Modifying property for robot {identifier} with args: {args}"
        )
        return self.lab_service.patch_object(identifier, COLLECTION, args)

    async def call_robot(
        self, identifier: str, args: ObjectCallRequest
    ) -> Dict[str, Any]:
        """
        Call a method on the robot.

        Args:
            identifier (str): The ID or name of the robot.
            args (ObjectCallRequest): The method call parameters.

        Returns:
            Dict[str, Any]: A dict representing the Operation model in JSON format.
        """
        op = self.lab_service.call_on_object(identifier, "robot", args)
        self._logger.debug(f"Calling robot {identifier} with args: {args}")
        self.scheduler.add_operation(op)
        return op.get_base_model().model_dump(mode="json")

    async def get_robot(self, identifier: str) -> DataModel:
        """
        Get a robot by its ID or name.

        Args:
            identifier (str): The ID or name of the robot.

        Returns:
            DataModel: The robot data model.
        """
        if is_valid_uuid(identifier):
            robot_obj = self.lab_service.get_object_by_id(identifier, COLLECTION)
        else:
            robot_obj = self.lab_service.get_object_by_name(identifier, COLLECTION)
        self._logger.debug(f"Getting robot with identifier: {identifier}")
        return convert_to_data_model(robot_obj)

    async def delete_robot(self, identifier: str) -> Dict:
        """
        Delete a robot by its ID or name.

        Args:
            identifier (str): The ID or name of the robot.

        Returns:
            Dict: A message indicating the result of the deletion.
        """
        self._logger.debug(f"Deleting robot with identifier: {identifier}")
        self.lab_service.delete_object(identifier, COLLECTION)
        return {"message": "Robot deleted successfully"}
