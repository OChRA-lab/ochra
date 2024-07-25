import pytest
from unittest.mock import MagicMock, patch
from ochra_common.connections.station_connection import StationConnection
from ochra_common.connections.rest_adapter import LabEngineException


@pytest.fixture
def mock_rest_adapter():
    with patch('ochra_common.connections.rest_adapter.RestAdapter') as mock_adapter:
        yield mock_adapter


@pytest.fixture
def station_connection():
    return StationConnection(hostname="test_host", api_key="test_key", ssl_verify=False)


def test_execute_op(station_connection, mock_rest_adapter):
    with pytest.raises(LabEngineException):
        mock_result = MagicMock(data="success")
        mock_rest_adapter.post.return_value = mock_result
        result = station_connection.execute_op(
            op="start", deviceName="test_device", param1="value1")
        mock_rest_adapter.return_value.post.assert_called_once_with(
            endpoint="process_op",
            data={"operation": "start",
                "deviceName": "test_device",
                "args": {"param1": "value1"}}
        )
        assert result == "success"

