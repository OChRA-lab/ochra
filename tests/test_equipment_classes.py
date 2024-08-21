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
    assert operation.result == []

    # test operation methods
    start_timestamp = datetime.now()
    end_timestamp = datetime.now() + timedelta(minutes=1)
    operation.add_start_timestamp(start_timestamp)
    operation.add_end_timestamp(end_timestamp)

    assert operation.to_dict() == {"id": operation.id.hex,
                                   "_collection": "operations",
                                   "_cls": "Operation",
                                   "caller_id": caller_id.hex,
                                   "method": "test_method",
                                   "args": {"arg": 1},
                                   "status": -1,
                                   "start_timestamp": start_timestamp.isoformat(),
                                   "end_timestamp": end_timestamp.isoformat(),
                                   "result": []}

    assert operation.to_json() == '{"id": "' + operation.id.hex + \
        '", "_collection": "operations", "_cls": "Operation", "caller_id": "' + \
        caller_id.hex + '", "method": "test_method", "args": {"arg": 1}, "status": -1, ' + \
        '"start_timestamp": "' + start_timestamp.isoformat() + '", "end_timestamp": "' + \
        end_timestamp.isoformat() + '", "result": []}'


def test_operation_result():
    # test construction of the operation result
    result = OperationResult(type="test", data=bytes(b"test"))

    # test operation result attributes
    assert result.id is not None
    assert result.type == "test"
    assert result.id is not None
    assert result._cls == "OperationResult"
    assert result._collection == "operation_results"
    assert result.data == bytes(b"test")

    # test operation result methods
    assert result.to_dict() == {"id": result.id.hex,
                                "_collection": "operation_results",
                                "_cls": "OperationResult",
                                "type": "test",
                                "data": b"test".hex()}

    assert result.to_json() == '{"id": "' + result.id.hex + \
        '", "_collection": "operation_results", "_cls": "OperationResult", "type": "test", "data": "74657374"}'


def test_device():
    # test construction of the device
    device = Device(name="test_device")

    # test device attributes
    assert device.id is not None
    assert device.name == "test_device"
    assert device.inventory == None
    assert device.status == -1
    assert device.station_id == ""
    assert device.operation_history == []

    # test device methods
    assert device.to_dict() == {"id": device.id.hex,
                                "_collection": "devices",
                                "_cls": "Device",
                                "name": "test_device",
                                "inventory": None,
                                "status": -1,
                                "station_id": "",
                                "operation_history": []}

    assert device.to_json() == '{"id": "' + device.id.hex + \
        '", "_collection": "devices", "_cls": "Device", "name": "test_device", "inventory": null,' + \
        ' "status": -1, "operation_history": [], "station_id": ""}'
