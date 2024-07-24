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

