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
        {"_collection": collection}, {"id": "test", "otherValue": "otherValue"})
    assert returnValue == "test"

    with pytest.raises(JSONDecodeError):
        mock_call.object_json = "invalid_json"
        labservice.construct_object(mock_call, collection)


def test_call_on_object(service):
    pass


def test_get_device():
    pass


def test_get_object_property():
    pass


def test_get_object_by_name():
    pass
