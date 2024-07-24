import pytest
from unittest.mock import MagicMock
from ochra_common.connections.lab_connection import LabConnection


@pytest.fixture
def lab_connection():
    with pytest.MonkeyPatch.context() as mocker:
        mock_rest_adapter = MagicMock()
        mocker.setattr("ochra_common.connections.lab_connection.RestAdapter",
                  lambda *args, **kwargs: mock_rest_adapter)
        lab_conn = LabConnection(hostname="test_host", api_key="test_key", ssl_verify=True, logger=None)
    return lab_conn, mock_rest_adapter

def test_construct_object(lab_connection):
    lab_conn, mock_rest_adapter = lab_connection
    mock_rest_adapter.post.return_value = MagicMock(data="mocked_construct_result")
    result = lab_conn.construct_object(
        object_type=str, catalogue_module="test_module", param="test_value")
    mock_rest_adapter.post.assert_called_once_with(
        endpoint="object/construct",
        data={
            "object_type": "str",
            "catalogue_module": "test_module",
            "contstructor_params": {"param": "test_value"}
        }
    )
    assert result == "mocked_construct_result"