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
    result = lab_conn.construct_object(object_type=str, catalogue_module="test_module", param1="test_value")
    mock_rest_adapter.construct.assert_called_once_with(
        object_type=str, catalogue_module="test_module", param1="test_value")
    assert result == "mocked_construct_result"

