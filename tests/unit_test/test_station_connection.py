import pytest
from unittest.mock import patch
from ochra_manager.connections.station_connection import StationConnection
from ochra_common.equipment.operation import Operation
from ochra_common.connections.rest_adapter import Result
from uuid import uuid4


@patch("ochra_manager.connections.station_connection.RestAdapter")
def test_execute_op(MockRestAdapter):
    station_conn = StationConnection()
    mock_rest = MockRestAdapter.return_value
    fake_result = Result(status_code=200, message="", data="test_result")
    mock_rest.post.return_value = fake_result

    op = Operation(caller_id=uuid4(), method="test_op", args={"param1": "value1"})
    result = station_conn.execute_op(op)

    mock_rest.post.assert_called_once_with(
        endpoint="process_op",
        data={
            "id": str(op.id),
            "caller_id": str(op.caller_id),
            "method": op.method,
            "args": op.args,
        },
    )
    assert result == fake_result
