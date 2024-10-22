from ochra_common.equipment.operation import Operation
from ochra_common.equipment.operation_result import OperationResult
from ochra_common.equipment.device import Device

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
    assert operation.status == -1
    assert operation.start_timestamp == None
    assert operation.end_timestamp == None
    assert operation.result == ""

    # test operation methods
    start_timestamp = datetime.now()
    end_timestamp = datetime.now() + timedelta(minutes=1)
    operation.start_timestamp = start_timestamp
    operation.end_timestamp = end_timestamp

    assert operation.model_dump() == {"id": operation.id,
                                   "cls": "Operation",
                                   "module_path": None,
                                   "caller_id": caller_id,
                                   "method": "test_method",
                                   "args": {"arg": 1},
                                   "status": -1,
                                   "start_timestamp": start_timestamp,
                                   "end_timestamp": end_timestamp,
                                   "result": ""}

    assert operation.model_dump_json() == '{"id":"' + str(operation.id) + \
        '","cls":"Operation","module_path":null,"caller_id":"' + \
        str(caller_id) + '","method":"test_method","args":{"arg":1},"status":-1,' + \
        '"start_timestamp":"' + start_timestamp.isoformat() + '","end_timestamp":"' + \
        end_timestamp.isoformat() + '","result":""}'


def test_operation_result():
    # test construction of the operation result
    entry_id = uuid.uuid4()
    result = OperationResult(type="test", data_entry_id=entry_id)

    # test operation result attributes
    assert result.id is not None
    assert result.type == "test"
    assert result.id is not None
    assert result.cls == "OperationResult"
    assert result.module_path == None
    assert result.data_entry_id == entry_id

    # test operation result methods
    assert result.model_dump() == {"id": result.id,
                                "cls": "OperationResult",
                                "module_path": None,
                                "type": "test",
                                "data_entry_id": entry_id}

    assert result.model_dump_json() == '{"id":"' + str(result.id) + \
        '","cls":"OperationResult","module_path":null,"type":"test","data_entry_id":"' + \
        str(entry_id) + '"}'


def test_device():
    # test construction of the device
    device = Device(name="test_device")

    # test device attributes
    assert device.id is not None
    assert device.name == "test_device"
    assert device.inventory == None
    assert device.status == -1
    assert device.station_id == None
    assert device.operation_history == []

    # test device methods
    assert device.model_dump() == {"id": device.id,
                                "cls": "Device",
                                "module_path": None,
                                "name": "test_device",
                                "inventory": None,
                                "status": -1,
                                "station_id": None,
                                "operation_history": []}

    assert device.model_dump_json() == '{"id":"' + str(device.id) + \
        '","cls":"Device","module_path":null,"name":"test_device","inventory":null,' + \
        '"status":-1,"operation_history":[],"station_id":null}'
