import pytest
from unittest.mock import MagicMock, patch
from ochra_manager.lab.lab_service import lab_service
from pydantic import BaseModel
from typing import Dict, Any
from fastapi import HTTPException
import json
from json.decoder import JSONDecodeError
from uuid import UUID
from requests import Response
from ochra_manager.connections.station_connection import StationConnection


class ObjectCallRequest(BaseModel):
    method: str
    args: Dict | None = None


class ObjectCallResponse(BaseModel):
    return_data: Any
    status_code: int
    msg: str


class ObjectQueryResponse(BaseModel):
    id: UUID
    cls: str


class ObjectPropertySetRequest(BaseModel):
    property: str
    property_value: Any


class ObjectConstructionRequest(BaseModel):
    object_json: str


@pytest.fixture
def service():
    with pytest.MonkeyPatch.context() as mocker:
        mock_db_conn = MagicMock()
        mocker.setattr("ochra_manager.connections.db_connection.DbConnection",
                       lambda *args, **kwargs: mock_db_conn)
        service = lab_service()
        service.db_conn = mock_db_conn
    return service, mock_db_conn


def test_patch_object(service):
    labservice: lab_service = service[0]
    mock_db_conn: MagicMock = service[1]

    object_id = "test_id"
    collection = "test_collection"
    mock_call = ObjectPropertySetRequest(
        property="test_property", property_value="test_value")

    labservice.patch_object(object_id, collection, mock_call)

    mock_db_conn.read.assert_called_once_with(
        {"id": object_id, "_collection": collection})
    mock_db_conn.update.assert_called_once_with({"id": object_id, "_collection": collection},
                                                {mock_call.property: mock_call.property_value})

    # error in update returns 500
    mock_db_conn.update.side_effect = Exception("test_exception")
    with pytest.raises(HTTPException) as e:
        labservice.patch_object(object_id, collection, mock_call)
    assert e.value.status_code == 500

    # error in read returns 404
    mock_db_conn.read.side_effect = Exception("test_exception")
    with pytest.raises(HTTPException) as e:
        labservice.patch_object(object_id, collection, mock_call)
    assert e.value.status_code == 404


def test_construct_object(service):
    labservice: lab_service = service[0]
    mock_db_conn: MagicMock = service[1]

    mock_call = ObjectConstructionRequest(
        object_json=json.dumps({"id": "test", "otherValue": "otherValue"}))

    collection = "test_collection"
    returnValue = labservice.construct_object(mock_call, collection)
    mock_db_conn.create.assert_called_once_with(
        {"_collection": collection},
        {"id": "test", "otherValue": "otherValue"})
    assert returnValue == "test"

    with pytest.raises(JSONDecodeError):
        mock_call.object_json = "invalid_json"
        labservice.construct_object(mock_call, collection)


def test_call_on_object(service):
    labservice: lab_service = service[0]
    mock_db_conn: MagicMock = service[1]

    mock_call = ObjectCallRequest(method="test_method", args={
                                  "test_arg": "test_value"})
    object_id = "test_id"
    collection = "test_collection"

    mock_db_conn.read.return_value = "test_object_name"
    res = Response()
    res.status_code = 200
    res.data = "test_result"
    res.message = ""
    with patch.object(StationConnection, "execute_op", return_value=res) as MockStationConnection:
        returnVal = labservice.call_on_object(object_id, collection, mock_call)
        MockStationConnection.assert_called_once_with("test_method", "test_object_name",
                                                      test_arg="test_value")
        assert returnVal.return_data == "test_result"
        assert returnVal.status_code == 200
        assert returnVal.msg == ""

        mock_db_conn.read.return_value = "test_object_name"
        # error in execute_op returns 500
        MockStationConnection.side_effect = [Exception(
            "test_exception_mock_station")]
        with pytest.raises(HTTPException) as e:
            labservice.call_on_object(object_id, collection, mock_call)
        assert e.value.status_code == 500
        assert e.value.detail == "test_exception_mock_station"

        # error in read returns 404
        mock_db_conn.read.return_value = None
        with pytest.raises(HTTPException) as e:
            labservice.call_on_object(object_id, collection, mock_call)
        assert e.value.status_code == 404


def test_get_object_property(service):
    labservice: lab_service = service[0]
    mock_db_conn: MagicMock = service[1]

    object_id = "test_id"
    collection = "test_collection"
    property = "test_property"

    mock_db_conn.read.return_value = "test_value"
    returnVal = labservice.get_object_property(object_id, collection, property)
    assert returnVal == "test_value"
    mock_db_conn.read.assert_called_once()

    mock_db_conn.read.side_effect = Exception("test_exception")
    with pytest.raises(HTTPException) as e:
        labservice.get_object_property(object_id, collection, property)
    assert e.value.status_code == 404


def test_get_object_by_name(service):
    labservice: lab_service = service[0]
    mock_db_conn: MagicMock = service[1]

    object_name = "test_name"
    collection = "test_collection"
    mock_db_conn.find.return_value = "test_id"
    returnVal = labservice.get_object_by_name(object_name, collection)
    assert returnVal == "test_id"
    mock_db_conn.find.assert_called_once()

    mock_db_conn.find.side_effect = Exception("test_exception")
    with pytest.raises(HTTPException) as e:
        labservice.get_object_by_name(object_name, collection)
    assert e.value.status_code == 404
