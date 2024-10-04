import pytest
from unittest.mock import MagicMock, patch
from ochra_manager.lab.lab_service import LabService
from typing import Dict, Any
from fastapi import HTTPException
import json
from json.decoder import JSONDecodeError
from ochra_common.connections.api_models import (
    ObjectPropertySetRequest, ObjectConstructionRequest, ObjectCallRequest, ObjectCallResponse)
from ochra_common.connections.rest_adapter import Result


@pytest.fixture
@patch("ochra_manager.lab.lab_service.DbConnection")
def mock_service(MockDbConnection):
    service = LabService()
    mock_db_conn = MockDbConnection.return_value
    return service, mock_db_conn


def test_patch_object(mock_service):
    lab_service: LabService = mock_service[0]
    mock_db_conn: MagicMock = mock_service[1]

    object_id = "727d1936-9022-453a-adc5-036d7dc72c0e"
    collection = "test_collection"
    mock_call = ObjectPropertySetRequest(
        property="test_property", property_value="test_value")

    lab_service.patch_object(object_id, collection, mock_call)

    mock_db_conn.read.assert_called_once_with(
        {"id": object_id, "_collection": collection})
    mock_db_conn.update.assert_called_once_with({"id": object_id, "_collection": collection},
                                                {mock_call.property: mock_call.property_value})

    # error in update returns 500
    mock_db_conn.update.side_effect = Exception("test_exception")
    with pytest.raises(HTTPException) as e:
        lab_service.patch_object(object_id, collection, mock_call)
    assert e.value.status_code == 500

    # error in read returns 404
    mock_db_conn.read.side_effect = Exception("test_exception")
    with pytest.raises(HTTPException) as e:
        lab_service.patch_object(object_id, collection, mock_call)
    assert e.value.status_code == 404


def test_construct_object(mock_service):
    lab_service: LabService = mock_service[0]
    mock_db_conn: MagicMock = mock_service[1]

    mock_call = ObjectConstructionRequest(
        object_json=json.dumps({"id": "727d1936-9022-453a-adc5-036d7dc72c0e", "property": "value"}))

    collection = "test_collection"
    return_value = lab_service.construct_object(mock_call, collection)
    mock_db_conn.create.assert_called_once_with(
        {"_collection": collection},
        {"id": "727d1936-9022-453a-adc5-036d7dc72c0e", "property": "value"})
    assert return_value == "727d1936-9022-453a-adc5-036d7dc72c0e"

    with pytest.raises(JSONDecodeError):
        mock_call.object_json = "invalid_json"
        lab_service.construct_object(mock_call, collection)


@patch("ochra_manager.lab.lab_service.Operation")
@patch("ochra_manager.lab.lab_service.StationConnection")
def test_call_on_object(MockStationConnection, MockOperation, mock_service):
    lab_service: LabService = mock_service[0]
    mock_db_conn: MagicMock = mock_service[1]

    mock_call = ObjectCallRequest(method="test_method", args={
                                  "test_arg": "test_value"})
    object_id = "727d1936-9022-453a-adc5-036d7dc72c0e"
    collection = "devices"

    mock_db_conn.read.side_effect = [
        "station_id", "station_ip", None, Exception("error")]
    mock_station_conn = MockStationConnection.return_value
    mock_station_conn.execute_op.return_value = Result(
        status_code=200, data="test_result", message="")

    result = lab_service.call_on_object(object_id, collection, mock_call)

    MockStationConnection.assert_called_once_with("station_ip:8000")
    MockOperation.assert_called_once_with(
        caller_id=object_id, method=mock_call.method, args=mock_call.args)
    mock_op = MockOperation.return_value
    mock_station_conn.execute_op.assert_called_once_with(mock_op)

    assert isinstance(result, ObjectCallResponse)
    assert result.return_data == "test_result"
    assert result.warnings == None

    # error in read returns 404
    with pytest.raises(HTTPException) as e:
        lab_service.call_on_object(object_id, collection, mock_call)
    assert e.value.status_code == 404

    # error in execute_op returns 500
    with pytest.raises(HTTPException) as e:
        lab_service.call_on_object(object_id, collection, mock_call)
    assert e.value.status_code == 500
    assert e.value.detail == "error"



def test_get_object_property(mock_service):
    lab_service: LabService = mock_service[0]
    mock_db_conn: MagicMock = mock_service[1]

    object_id = "727d1936-9022-453a-adc5-036d7dc72c0e"
    collection = "test_collection"
    property = "test_property"

    mock_db_conn.read.return_value = "test_value"
    return_val = lab_service.get_object_property(
        object_id, collection, property)
    assert return_val == "test_value"
    mock_db_conn.read.assert_called_once_with(
        {"id": object_id, "_collection": collection}, property)

    mock_db_conn.read.side_effect = Exception("test_exception")
    with pytest.raises(HTTPException) as e:
        lab_service.get_object_property(object_id, collection, property)
    assert e.value.status_code == 404


def test_get_object_by_name(mock_service):
    lab_service: LabService = mock_service[0]
    mock_db_conn: MagicMock = mock_service[1]

    object_name = "test_name"
    collection = "test_collection"
    object_json = '{"id": 727d1936-9022-453a-adc5-036d7dc72c0e, "name": "test_name"}'
    mock_db_conn.find.return_value = object_json
    return_val = lab_service.get_object_by_name(object_name, collection)
    mock_db_conn.find.assert_called_once_with(
        {"_collection": collection}, {"name": object_name})
    assert return_val == object_json

    mock_db_conn.find.side_effect = Exception("test_exception")
    with pytest.raises(HTTPException) as e:
        lab_service.get_object_by_name(object_name, collection)
    assert e.value.status_code == 404


def test_get_object_by_id(mock_service):
    lab_service: LabService = mock_service[0]
    mock_db_conn: MagicMock = mock_service[1]

    object_id = "727d1936-9022-453a-adc5-036d7dc72c0e"
    collection = "test_collection"
    object_json = '{"id": 727d1936-9022-453a-adc5-036d7dc72c0e, "name": "test_name"}'
    mock_db_conn.find.return_value = object_json
    return_val = lab_service.get_object_by_id(object_id, collection)
    mock_db_conn.find.assert_called_once_with(
        {"_collection": collection}, {"id": object_id})
    assert return_val == object_json

    mock_db_conn.find.side_effect = Exception("test_exception")
    with pytest.raises(HTTPException) as e:
        lab_service.get_object_by_name(object_id, collection)
    assert e.value.status_code == 404


def test_get_object_by_station_and_type(mock_service):
    lab_service: LabService = mock_service[0]
    mock_db_conn: MagicMock = mock_service[1]

    # test station identifier is a uuid
    station_id = "727d1936-1111-453a-aaaa-036d7dc72c0e"
    collection = "test_collection"
    obj_type = "test_type"
    object_json = '{"id": 727d1936-9022-453a-adc5-036d7dc72c0e, "name": "test_name"}'
    mock_db_conn.find.return_value = object_json
    return_val = lab_service.get_object_by_station_and_type(
        station_id, collection, obj_type)
    mock_db_conn.find.assert_called_once_with({"_collection": collection}, {
                                              "station_id": station_id, "_cls": obj_type})
    assert return_val == object_json

    # test station identifier is a name
    station_name = "test_station"
    mock_db_conn.find.reset_mock()
    mock_db_conn.find.side_effect = [
        "727d1936-1111-453a-aaaa-036d7dc72c0e", object_json, Exception("test_exception")]
    return_val = lab_service.get_object_by_station_and_type(
        station_name, collection, obj_type)
    mock_db_conn.find.assert_called_with({"_collection": collection}, {
                                         "station_id": station_id, "_cls": obj_type})
    assert return_val == object_json

    with pytest.raises(HTTPException) as e:
        lab_service.get_object_by_station_and_type(
            station_id, collection, obj_type)
    assert e.value.status_code == 404
