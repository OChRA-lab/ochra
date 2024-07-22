import pytest
import logging
from unittest.mock import MagicMock
from ochra_common.connections.lab_connection import LabConnection

@pytest.fixture
def lab_connection():
    # Mock the RestAdapter used in LabConnection
    with pytest.MonkeyPatch.context() as m:
        mock_rest_adapter = MagicMock()
        mock_logger = MagicMock(spec=logging.Logger)
        m.setattr("ochra_common.connections.rest_adapter.RestAdapter",
                  lambda *args, **kwargs: mock_rest_adapter)
    # Create an instance of LabConnection with the mocked adapter
    lab_conn = LabConnection(hostname="test_host", api_key="test_key", ssl_verify=True, logger=mock_logger)
    return lab_conn, mock_rest_adapter

def test_construct_object(lab_connection):
    lab_conn, mock_rest_adapter = lab_connection
    mock_rest_adapter.construct.return_value = "mocked_construct_result"
    result = lab_conn.construct_object("test_type", "test_module", "test_value")
    mock_rest_adapter.construct.assert_called_once_with(
        "test_type", "test_module", "test_value")
    assert result == "mocked_construct_result"
    
def test_call_on_object(lab_connection):
    lab_conn, mock_rest_adapter = lab_connection
    mock_rest_adapter.call.return_value = "mocked_call_result"
    result = lab_conn.call_on_object("test_id", "test_function", "test_value")
    mock_rest_adapter.call.assert_called_once_with(
        "test_id", "test_function", "test_value")
    assert result == "mocked_call_result"

def test_get_object(lab_connection):
    lab_conn, mock_rest_adapter = lab_connection
    mock_rest_adapter.get.return_value = "mocked_get_result"
    result = lab_conn.get_object("test_id")
    mock_rest_adapter.get.assert_called_once_with("test_id")
    assert result == "mocked_get_result"
    
def test_patch_object(lab_connection):
    lab_conn, mock_rest_adapter = lab_connection
    mock_rest_adapter.patch.return_value = "mocked_patch_result"
    result = lab_conn.patch_object("test_id", "test_value")
    mock_rest_adapter.patch.assert_called_once_with("test_id", "test_value")
    assert result == "mocked_patch_result"
    
def test_create_station(lab_connection):
    lab_conn, mock_rest_adapter = lab_connection
    mock_rest_adapter.create_station.return_value = "mocked_create_station_result"
    result = lab_conn.create_station()
    mock_rest_adapter.create_station.assert_called_once_with()
    assert result == "mocked_create_station_result"

