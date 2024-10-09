import pytest
from unittest.mock import MagicMock, patch
from ochra_common.connections.lab_connection import LabConnection
from ochra_common.connections.rest_adapter import LabEngineException, Result
from uuid import UUID, uuid4
from pydantic import BaseModel, Field


class TestDataModel(BaseModel):
    id: UUID = Field(default_factory=uuid4)
    cls: str = Field(default=None)
    params: dict = Field(default=None)
    objects: list = Field(default=None)
    _endpoint = "test_type"

    @classmethod
    def from_id(cls, id):
        return cls(id=id)


@pytest.fixture
@patch("ochra_common.connections.lab_connection.RestAdapter")
def mock_connection(MockRestAdapter):
    lab_conn = LabConnection(hostname="test_host",
                             api_key="test_key", ssl_verify=False)
    lab_conn.rest_adapter = MockRestAdapter
    return lab_conn, MockRestAdapter


def test_construct_object(mock_connection):
    lab_conn, mock_rest = mock_connection

    test_data = TestDataModel(cls="test_type", params={"param": "value"})
    fake_result = Result(status_code=200, message="success",
                         data=str(test_data.id))
    mock_rest.put.return_value = fake_result

    result = lab_conn.construct_object("test_type", test_data)
    mock_rest.put.assert_called_once_with(
        "/test_type/construct",
        data={
            "object_json": test_data.model_dump_json()
        },
    )
    assert result == test_data.id

    mock_rest.put.return_value = MagicMock(data="invalid_data")
    with pytest.raises(LabEngineException):
        lab_conn.construct_object("test_type", test_data)


def test_get_object_by_name(mock_connection):
    lab_conn, mock_rest = mock_connection

    id = uuid4()
    fake_result = Result(status_code=200, message="success",
                         data={"id": str(id), "cls": "ochra_common.equipment.device.Device"})

    mock_rest.get.return_value = fake_result
    with patch("ochra_common.equipment.device.Device", TestDataModel()) as mock_device:
        result = lab_conn.get_object("test_type", "test_name")
        mock_rest.get.assert_called_once_with(
            "/test_type/get/test_name")
        assert result.id == id
        assert isinstance(result, TestDataModel)
        mock_rest.get.return_value = MagicMock(data="invalid_data")
        with pytest.raises(LabEngineException):
            lab_conn.get_object("test_type", "test_name")


def test_get_object_by_uuid(mock_connection):
    lab_conn, mock_rest = mock_connection

    id = uuid4()
    fake_result = Result(status_code=200, message="success",
                         data={"id": str(id), "cls": "ochra_common.equipment.device.Device"})

    mock_rest.get.return_value = fake_result
    with patch("ochra_common.equipment.device.Device", TestDataModel()) as mock_device:
        result = lab_conn.get_object("test_type", id)

        mock_rest.get.assert_called_once_with(f"/test_type/get/{id}")
        assert result.id == id
        assert isinstance(result, TestDataModel)

        mock_rest.get.return_value = MagicMock(data="invalid_data")
        with pytest.raises(LabEngineException):
            lab_conn.get_object("test_type", id)


def test_delete_object(mock_connection):
    lab_conn, mock_rest = mock_connection

    id = uuid4()

    fake_result = Result(status_code=200, data="deleted")
    mock_rest.delete.return_value = fake_result

    result = lab_conn.delete_object("test_type", id)
    mock_rest.delete.assert_called_once_with(f"/test_type/delete/{id}")
    assert result == "deleted"


def test_call_on_object(mock_connection):
    lab_conn, mock_rest = mock_connection

    id = uuid4()
    operation_id = uuid4()
    fake_result = Result(status_code=200, message="success",
                         data=str(operation_id))
    mock_rest.post.return_value = fake_result

    with patch("ochra_common.equipment.operation_proxy.OperationProxy", TestDataModel()) as mock_operation:
        result = lab_conn.call_on_object(
            "test_type", id, "test_method", {"arg": "value"})

        mock_rest.post.assert_called_once_with(
            f"/test_type/{id}/call_method",
            data={"method": "test_method", "args": {"arg": "value"}},
        )
        assert isinstance(result, TestDataModel)
        assert result.id == operation_id

        mock_rest.post.return_value = MagicMock(data="invalid_data")
        with pytest.raises(LabEngineException):
            lab_conn.call_on_object(
                "test_type", UUID(f"{id}"), "test_method", {"arg": "value"}
            )


def test_get_object_query_response_property(mock_connection):
    lab_conn, mock_rest = mock_connection

    id = uuid4()
    fake_result = Result(status_code=200, data={
                         "id": str(id), "cls": "ochra_common.equipment.device.Device"})
    mock_rest.get.return_value = fake_result
    with patch("ochra_common.equipment.device.Device", TestDataModel()) as mock_device:
        result = lab_conn.get_property("stations", id, "name")

        mock_rest.get.assert_called_once_with(
            f"/stations/{id}/get_property/name")

        assert result.id == id
        assert isinstance(result, TestDataModel)

        mock_rest.get.return_value = MagicMock(
            data="invalid_data", status_code=404)
        with pytest.raises(LabEngineException):
            lab_conn.get_property("stations", id, "name")


def test_get_object_query_response_list_property(mock_connection):
    lab_conn, mock_rest = mock_connection

    id = uuid4()
    id2 = uuid4()
    fake_result = Result(status_code=200, data=[{"id": str(id), "cls": "ochra_common.equipment.device.Device"},
                         {"id": str(id2), "cls": "ochra_common.equipment.device.Device"}])
    mock_rest.get.return_value = fake_result
    with patch("ochra_common.equipment.device.Device", TestDataModel()) as mock_device:
        result = lab_conn.get_property("stations", id, "objects")

        mock_rest.get.assert_called_once_with(
            f"/stations/{id}/get_property/objects")

        assert len(result) == 2
        assert result[0].id == id
        assert result[1].id == id2
        assert isinstance(result[0], TestDataModel)
        assert isinstance(result[1], TestDataModel)
        
        mock_rest.get.return_value = MagicMock(
            data="invalid_data", status_code=404)
        with pytest.raises(LabEngineException):
            lab_conn.get_property("stations", id, "name")


def test_get_property(mock_connection):
    lab_conn, mock_rest = mock_connection

    id = uuid4()
    fake_result = Result(status_code=200, data={"number": 42})
    mock_rest.get.return_value = fake_result

    result = lab_conn.get_property("stations", id, "map")

    mock_rest.get.assert_called_once_with(
        f"/stations/{id}/get_property/map")

    assert result == {"number": 42}

    mock_rest.get.return_value = MagicMock(
        data="invalid_data", status_code=404)
    with pytest.raises(LabEngineException):
        lab_conn.get_property("stations", id, "name")


def test_get_list_property(mock_connection):
    lab_conn, mock_rest = mock_connection

    id = uuid4()
    fake_result = Result(status_code=200, data=[1, 2, 3])
    mock_rest.get.return_value = fake_result

    result = lab_conn.get_property("stations", id, "list")

    mock_rest.get.assert_called_once_with(
        f"/stations/{id}/get_property/list")

    assert result == [1, 2, 3]

    mock_rest.get.return_value = MagicMock(
        data="invalid_data", status_code=404)
    with pytest.raises(LabEngineException):
        lab_conn.get_property("stations", id, "name")


def test_set_property(mock_connection):
    lab_conn, mock_rest = mock_connection

    id = uuid4()
    fake_result = Result(status_code=200, data="property_set")
    mock_rest.patch.return_value = fake_result

    result = lab_conn.set_property(
        "stations", id, "test_property", "new_value")
    mock_rest.patch.assert_called_once_with(
        f"/stations/{id}/modify_property",
        data={"property": "test_property", "property_value": "new_value"},
    )
    assert result == "property_set"
