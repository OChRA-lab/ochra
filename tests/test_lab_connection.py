import pytest
from unittest.mock import MagicMock
from ochra_common.connections.lab_connection import LabConnection
from ochra_common.connections.rest_adapter import LabEngineException, RestAdapter
from uuid import UUID, uuid4
import json
from pydantic import BaseModel, Field, ValidationError


@pytest.fixture
def lab_connection():
    with pytest.MonkeyPatch.context() as mocker:
        mock_rest = MagicMock()
        mocker.setattr("ochra_common.connections.rest_adapter.RestAdapter",
                       lambda *args, **kwargs: mock_rest)
        lab_conn = LabConnection(hostname="test_host",
                                 api_key="test_key", ssl_verify=False)
        lab_conn.rest_adapter = mock_rest
    return lab_conn, mock_rest


class TestDataModel(BaseModel):
    id: UUID = Field(default_factory=uuid4)
    cls: str = Field(default=None)
    params: dict = Field(default=None)


def test_construct_object(lab_connection):
    lab_conn, mock_rest = lab_connection

    test_data = TestDataModel(cls="test_type", params={"param": "value"})
    mock_result = MagicMock(data=str(test_data.id))
    mock_result.json.return_value = {
        "data": str(test_data.id)}
    mock_rest.put.return_value = mock_result

    result = lab_conn.construct_object("test_type", test_data)
    mock_rest.put.assert_called_once_with(
        "/test_type/construct",
        data={"object_json": '{"id":"'+str(test_data.id)+'","cls":"test_type","params":{"param":"value"}}'}
    )
    assert result == UUID(str(test_data.id))

    mock_rest.put.return_value = MagicMock(data="invalid_data")
    with pytest.raises(LabEngineException):
        lab_conn.construct_object("test_type", test_data)


def test_get_object_by_name(lab_connection):
    lab_conn, mock_rest = lab_connection

    id = uuid4()

    mock_result = MagicMock(data={"id": str(id), "cls": "test_cls"})
    mock_rest.get.return_value = mock_result

    result = lab_conn.get_object("test_type", "test_name")
    mock_rest.get.assert_called_once_with(
        "/test_type/get", {"name": "test_name"})
    assert result.id == id
    assert result.cls == "test_cls"

    mock_rest.get.return_value = MagicMock(data="invalid_data")
    with pytest.raises(LabEngineException):
        lab_conn.get_object("test_type", "test_name")


def test_get_object_by_uuid(lab_connection):
    lab_conn, mock_rest = lab_connection
    lab_conn.rest_adapter = mock_rest

    id = UUID("123e4567-e89b-12d3-a456-426614174000")

    mock_result = MagicMock(data={"id": str(id), "cls": "test_cls"})
    mock_rest.get.return_value = mock_result

    result = lab_conn.get_object(
        "test_type", UUID("123e4567-e89b-12d3-a456-426614174000"))
    mock_rest.get.assert_called_once_with(
        f"/test_type/get_by_id/{id}")
    assert result.id == id
    assert result.cls == "test_cls"

    mock_rest.get.return_value = MagicMock(data="invalid_data")
    with pytest.raises(LabEngineException):
        lab_conn.get_object("test_type", UUID(
            "123e4567-e89b-12d3-a456-426614174000"))


def test_delete_object(lab_connection):
    lab_conn, mock_rest = lab_connection

    id = UUID("123e4567-e89b-12d3-a456-426614174000")

    mock_result = MagicMock(data="deleted")
    mock_rest.delete.return_value = mock_result

    result = lab_conn.delete_object("test_type", id)
    mock_rest.delete.assert_called_once_with(
       f"/test_type/delete/{id}")
    assert result == "deleted"


def test_call_on_object(lab_connection):
    lab_conn, mock_rest = lab_connection

    id = UUID("123e4567-e89b-12d3-a456-426614174000")

    mock_result = MagicMock(
        data={"return_data": "called", "status_code": 200, "msg": "success"})
    mock_rest.post.return_value = mock_result

    result = lab_conn.call_on_object(
        "test_type", id, "test_method", {"arg": "value"})
    mock_rest.post.assert_called_once_with(
       f"/test_type/{id}/call_method", '{"method":"test_method","args":{"arg":"value"}}'
    )
    assert result.return_data == "called"
    assert result.status_code == 200
    assert result.msg == "success"

    mock_rest.post.return_value = MagicMock(data="invalid_data")
    with pytest.raises(LabEngineException):
        lab_conn.call_on_object("test_type", UUID(
            f"{id}"), "test_method", {"arg": "value"})


def test_get_property(lab_connection):
    lab_conn, mock_rest = lab_connection
    id = UUID("123e4567-e89b-12d3-a456-426614174000")
    mock_result = MagicMock(data={"id": str(id), "cls": "test_cls"})
    mock_rest.get.return_value = mock_result

    result = lab_conn.get_property("test_type", id, "test_property")
    mock_rest.get.assert_called_once_with(
        f"/test_type/{id}/get_property/test_property")
    assert result.id == id
    assert result.cls == "test_cls"
    # TODO: this currently doenst work but im unsure how the message gets returned anyway so ill come back to it
    mock_rest.get.return_value = MagicMock(data="property_value")

    result = lab_conn.get_property("test_type", id, "test_property")
    assert result == "property_value"

    mock_rest.get.return_value = MagicMock(
        data="invalid_data", status_code=404)
    with pytest.raises(LabEngineException):
        lab_conn.get_property("test_type", id, "test_property")


def test_set_property(lab_connection):
    lab_conn, mock_rest = lab_connection

    id = UUID("123e4567-e89b-12d3-a456-426614174000")

    mock_result = MagicMock(data="property_set")
    mock_rest.post.return_value = mock_result

    result = lab_conn.set_property("test_type", id, "test_property", "value")
    mock_rest.post.assert_called_once_with(
        f"/test_type/{id}/modify_property", '{"property":"test_property","property_value":"value"}'
    )
    assert result == "property_set"
