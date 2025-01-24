from ochra_common.equipment.operation import Operation
from ochra_common.equipment.operation_result import OperationResult
from ochra_common.equipment.device import Device
from ochra_common.equipment.robot import Robot
from ochra_common.equipment.mobile_robot import MobileRobot
from ochra_common.utils.enum import OperationStatus, ResultDataStatus, ActiveStatus, MobileRobotState

import uuid
from datetime import datetime, timedelta


def test_operation():
    # test construction of the operation
    caller_id = uuid.uuid4()
    operation = Operation(
        caller_id=caller_id,
        method="test_method",
        args={"arg": 1},
    )

    # test operation attributes
    assert operation.id is not None
    assert operation.caller_id == caller_id
    assert operation.method == "test_method"
    assert operation.args == {"arg": 1}
    assert operation.status == OperationStatus.CREATED
    assert operation.start_timestamp == None
    assert operation.end_timestamp == None
    assert operation.result == None

    # test operation methods
    start_timestamp = datetime.now()
    end_timestamp = datetime.now() + timedelta(minutes=1)
    operation.start_timestamp = start_timestamp
    operation.end_timestamp = end_timestamp

    assert operation.model_dump() == {
        "id": operation.id,
        "collection": None,
        "cls": "Operation",
        "module_path": None,
        "caller_id": caller_id,
        "method": "test_method",
        "args": {"arg": 1},
        "status": OperationStatus.CREATED,
        "start_timestamp": start_timestamp,
        "end_timestamp": end_timestamp,
        "result": None,
    }


def test_operation_result():
    # test construction of the operation result
    result = OperationResult(
        success=True,
        result_data=123,
        data_type="int",
        data_status=ResultDataStatus.AVAILABLE,
    )

    # test operation result attributes
    assert result.id is not None
    assert result.success
    assert result.result_data == 123
    assert result.cls == "OperationResult"
    assert result.data_type == "int"
    assert result.data_status == ResultDataStatus.AVAILABLE

    # test operation result methods
    assert result.model_dump() == {
        "id": result.id,
        "collection": None,
        "cls": "OperationResult",
        "module_path": None,
        "success": True,
        "error": "",
        "result_data": 123,
        "data_filename": "",
        "data_type": "int",
        "data_status": ResultDataStatus.AVAILABLE,
    }


def test_device():
    # test construction of the device
    device = Device(name="test_device")

    # test device attributes
    assert device.id is not None
    assert device.name == "test_device"
    assert device.inventory == None
    assert device.status == ActiveStatus.IDLE
    assert device.owner_station == None
    assert device.operation_history == []

    # test device methods
    assert device.model_dump() == {
        "id": device.id,
        "collection": None,
        "cls": "Device",
        "module_path": None,
        "name": "test_device",
        "inventory": None,
        "status": ActiveStatus.IDLE,
        "owner_station": None,
        "operation_history": [],
    }


def test_robot():
    # test construction of the robot
    robot = Robot(name="test_robot", available_tasks=["task1", "task2"])

    # test robot attributes
    assert robot.id is not None
    assert robot.name == "test_robot"
    assert robot.available_tasks == ["task1", "task2"]

    # test robot methods
    assert robot.model_dump() == {
        "id": robot.id,
        "collection": None,
        "cls": "Robot",
        "module_path": None,
        "name": "test_robot",
        "inventory": None,
        "status": ActiveStatus.IDLE,
        "owner_station": None,
        "operation_history": [],
        "available_tasks": ["task1", "task2"],
    }

def test_mobile_robot():
    # test construction of the robot
    robot = MobileRobot(name="test_robot", available_tasks=["task1", "task2"])

    # test robot attributes
    assert robot.id is not None
    assert robot.name == "test_robot"
    assert robot.available_tasks == ["task1", "task2"]
    assert robot.state == MobileRobotState.AVAILABLE

    # test robot methods
    assert robot.model_dump() == {
        "id": robot.id,
        "collection": None,
        "cls": "MobileRobot",
        "module_path": None,
        "name": "test_robot",
        "inventory": None,
        "status": ActiveStatus.IDLE,
        "state": MobileRobotState.AVAILABLE,
        "owner_station": None,
        "operation_history": [],
        "available_tasks": ["task1", "task2"],
    }
