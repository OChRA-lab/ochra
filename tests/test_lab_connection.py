import pytest
from unittest.mock import MagicMock, patch
from ochra_common.connections.lab_connection import LabConnection
from ochra_common.connections.rest_adapter import LabEngineException


@pytest.fixture
def mock_rest_adapter():
    with patch('ochra_common.connections.rest_adapter.RestAdapter') as mock_adapter:
        yield mock_adapter


@pytest.fixture
def lab_connection():
    return LabConnection(hostname="testhost", api_key="testkey", ssl_verify=False)


def test_construct_object(lab_connection, mock_rest_adapter):
    with pytest.raises(LabEngineException):
        mock_result = MagicMock(data={"id": "test_object_id"})
        mock_rest_adapter.post.return_value = mock_result
        result = lab_connection.construct_object(
            object_type=str, catalogue_module="test_module", param1="value1")
        mock_rest_adapter.post.assert_called_once_with(
            endpoint="object/construct",
            data={
                "object_type": "str",
                "catalogue_module": "test_module",
                "contstructor_params": {"param1": "value1"}
            }
        )
        assert result == {"id": "test_object_id"}


def test_call_on_object(lab_connection, mock_rest_adapter):
    with pytest.raises(LabEngineException):
        mock_result = MagicMock(data="function_called")
        mock_rest_adapter.post.return_value = mock_result
        result = lab_connection.call_on_object(
            object_id="test_id", object_function="test_function", arg1="value1")
        mock_rest_adapter.post.assert_called_once_with(
            endpoint=f"object/call/test_id",
            data={
                "object_function": "test_function",
                "args": {"arg1": "value1"}
            }
        )
        assert result.data == "function_called"
        
        
def test_get_object(lab_connection, mock_rest_adapter):
    with pytest.raises(LabEngineException):
        mock_result = MagicMock(data={"id": "test_id", "name": "test_name"})
        mock_rest_adapter.get.return_value = mock_result
        result = lab_connection.get_object(object_id="test_id")
        mock_rest_adapter.get.assert_called_once_with(endpoint=f"object/get/test_id")
        assert result == {"id": "test_id", "name": "test_name"}
 
def test_patch_object(lab_connection, mock_rest_adapter):
    with pytest.raises(LabEngineException):
        mock_result = MagicMock(data="object_patched")
        mock_rest_adapter.patch.return_value = mock_result
        result = lab_connection.patch_object(
            object_id="test_id", property1="value1")
        mock_rest_adapter.patch.assert_called_once_with(
            endpoint=f"object/set/test_id",
            data={"properties": {"property1": "value1"}}
        )
        assert result.data == "object_patched"
        