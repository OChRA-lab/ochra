import pytest
from unittest.mock import MagicMock
from ochra_common.connections.station_connection import StationConnection
from ochra_common.connections.rest_adapter import LabEngineException


@pytest.fixture
def station_connection():
    with pytest.MonkeyPatch.context() as mocker:
        mock_rest = MagicMock()
        mocker.setattr("ochra_common.connections.rest_adapter.RestAdapter",
                  lambda *args, **kwargs: mock_rest)
        station_conn = StationConnection(hostname="test_host", api_key="test_key", ssl_verify=False)
    return station_conn, mock_rest


def test_execute_op(station_connection):
    station_conn, mock_rest = station_connection
    with pytest.raises(LabEngineException):
        mock_result = MagicMock(data="success")
        mock_rest.post.return_value = mock_result
        result = station_conn.execute_op(
            op="start", deviceName="test_device", param1="value1")
        mock_rest.return_value.post.assert_called_once_with(
            endpoint="process_op",
            data={"operation": "start",
                "deviceName": "test_device",
                "args": {"param1": "value1"}}
        )
        assert result == "success"

