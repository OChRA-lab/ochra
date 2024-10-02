import pytest
from unittest.mock import MagicMock, patch
from ochra_manager.station.station_server import StationServer
from ochra_common.spaces.location import Location
from ochra_common.equipment.operation import Operation
from fastapi.testclient import TestClient
from uuid import uuid4

@patch("ochra_manager.station.station_server.WorkStation")
@patch("ochra_manager.station.station_server.LabConnection")
def test_setup(MockLab, MockWorkStationProxy):
    station_loc = Location(name="test_location", map="test_map", map_id=1)
    server = StationServer(name="test_station", location=station_loc)
    server.setup(lab_ip="1.2.3.4")

    MockLab.assert_called_once_with("1.2.3.4")
    MockWorkStationProxy.assert_called_once_with("test_station", station_loc)

    assert server._app is not None
    assert server._router is not None


def test_ping():
    server = StationServer(name="test_station",
                           location=Location(name="test_location", map="test_map", map_id=1))
    server.setup()

    client = TestClient(server._app)
    response = client.get("/ping")
    assert response.status_code == 200


@patch("ochra_manager.station.station_server.WorkStation")
@patch("ochra_manager.station.station_server.LabConnection")
def test_add_device(MockLab, MockWorkStationProxy):
    station_loc = Location(name="test_location", map="test_map", map_id=1)
    server = StationServer(name="test_station", location=station_loc)
    server.setup(lab_ip="1.2.3.4")

    device_id = uuid4()
    mock_device = MagicMock(spec=["id", "execute_operation"])
    mock_device.id = device_id

    server.add_device(mock_device)
    assert server._devices[device_id] == mock_device

    mock_station_proxy = server._station_proxy
    mock_station_proxy.add_device.assert_called_once_with(mock_device)


@patch("ochra_manager.station.station_server.WorkStation")
@patch("ochra_manager.station.station_server.LabConnection")
def test_process_op(MockLab, MockWorkStationProxy):
    station_loc = Location(name="test_location", map="test_map", map_id=1)
    server = StationServer(name="test_station", location=station_loc)
    server.setup(lab_ip="1.2.3.4")

    device_id = uuid4()
    mock_device = MagicMock(spec=["id", "execute_operation"])
    mock_device.id = device_id
    mock_device.execute_operation.return_value = True

    server.add_device(mock_device)

    op = Operation(caller_id=device_id,
                   method="execute_operation", args={"arg": 1})

    # This is done to handle fields that are None
    op_json = {"id": str(op.id), "caller_id": str(
        op.caller_id), "method": op.method, "args": op.args}
    
    client = TestClient(server._app)
    response = client.post(
        "/process_op", json=op_json)
    
    assert response.status_code == 200
    assert response.json() == True
    mock_device.execute_operation.assert_called_once_with(**op.args)

    # test for invalid operation
    op_json = {"id": str(op.id), "caller_id": str(
    op.caller_id), "method": "invalid_method", "args": op.args}

    response = client.post(
        "/process_op", json=op_json)

    assert response.status_code == 500

    # test for unavailable device
    op_json = {"id": str(op.id), "caller_id": str(
    uuid4()), "method": op.method, "args": op.args}

    response = client.post(
        "/process_op", json=op_json)

    assert response.status_code == 500

    

