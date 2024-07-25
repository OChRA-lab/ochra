import pytest
from unittest.mock import MagicMock
from ochra_common.connections.lab_connection import LabConnection
from ochra_common.connections.rest_adapter import LabEngineException


@pytest.fixture
def lab_connection():
    with pytest.MonkeyPatch.context() as mocker:
        mock_rest = MagicMock()
        mocker.setattr("ochra_common.connections.rest_adapter.RestAdapter",
                  lambda *args, **kwargs: mock_rest)
        lab_conn = LabConnection(hostname="testhost", api_key="testkey", ssl_verify=False)
    return lab_conn, mock_rest


def test_construct_object(lab_connection):
    lab_conn, mock_rest = lab_connection
    with pytest.raises(LabEngineException):
        mock_result = MagicMock(data={"id": "test_object_id"})
        mock_rest.post.return_value = mock_result
        result = lab_conn.construct_object(
            object_type=str, catalogue_module="test_module", param1="value1")
        mock_rest.post.assert_called_once_with(
            endpoint="object/construct",
            data={
                "object_type": "str",
                "catalogue_module": "test_module",
                "contstructor_params": {"param1": "value1"}
            }
        )
        assert result == {"id": "test_object_id"}


def test_call_on_object(lab_connection):
    lab_conn, mock_rest = lab_connection
    with pytest.raises(LabEngineException):
        mock_result = MagicMock(data="function_called")
        mock_rest.post.return_value = mock_result
        result = lab_conn.call_on_object(
            object_id="test_id", object_function="test_function", arg1="value1")
        mock_rest.post.assert_called_once_with(
            endpoint=f"object/call/test_id",
            data={
                "object_function": "test_function",
                "args": {"arg1": "value1"}
            }
        )
        assert result.data == "function_called"
        
        
def test_get_object(lab_connection):
    lab_conn, mock_rest = lab_connection
    with pytest.raises(LabEngineException):
        mock_result = MagicMock(data={"id": "test_id", "name": "test_name"})
        mock_rest.get.return_value = mock_result
        result = lab_conn.get_object(object_id="test_id")
        mock_rest.get.assert_called_once_with(endpoint=f"object/get/test_id")
        assert result == {"id": "test_id", "name": "test_name"}
 
 
def test_patch_object(lab_connection):
    lab_conn, mock_rest = lab_connection
    with pytest.raises(LabEngineException):
        mock_result = MagicMock(data="object_patched")
        mock_rest.patch.return_value = mock_result
        result = lab_conn.patch_object(
            object_id="test_id", property1="value1")
        mock_rest.patch.assert_called_once_with(
            endpoint=f"object/set/test_id",
            data={"properties": {"property1": "value1"}}
        )
        assert result.data == "object_patched"
        
        
def test_create_station(lab_connection):
    lab_conn, mock_rest = lab_connection
    with pytest.raises(LabEngineException):
        mock_result = MagicMock(data={"id": "new_station_id"})
        mock_result.data = {"id": "new_station_id"}
        mock_rest.post.return_value = mock_result
        result = lab_conn.create_station()
        mock_rest.post.assert_called_once_with(endpoint="station/create")
        assert result == {"id": "new_station_id"}
        