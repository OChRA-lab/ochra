import pytest
from unittest.mock import MagicMock
from ochra_manager.lab.lab_service import lab_service
from pydantic import BaseModel
from typing import Dict


class ObjectCallRequest(BaseModel):
    method: str
    args: Dict | None = None


class ObjectPropertySetRequest(BaseModel):
    property: str
    property_value: str


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


def test_construct_object():
    pass


def test_call_on_object():
    pass


def test_get_device():
    pass


def test_get_object_property():
    pass


def test_get_object_by_name():
    pass
