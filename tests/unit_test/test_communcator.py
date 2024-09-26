import pytest
from unittest.mock import MagicMock, patch
from ochra_manager.Station.communicator import Communicator
from pydantic import BaseModel
from ochra_common.connections.lab_connection import LabConnection
from typing import Dict, Any, Optional


class MockDevice(BaseModel):
    name: str
    type: str
    id: str

    def mock_process(self, **kwargs):
        return kwargs


class operationExecute(BaseModel):
    operation: str
    deviceName: str
    args: Optional[Dict] = None


def test_process_operation():
    communicator = Communicator()
    with patch("ochra_common.connections.lab_connection.LabConnection") as mock:
        mock.return_value = MagicMock()

        def mock_start_up():
            pass

        communicator._start_up = mock_start_up
        communicator.setup_server()

        communicator._devices.append(MockDevice(
            name="test", type="test", id="test"))

        mock_call = operationExecute(
            operation="mock_process", deviceName="test", args={"test": "test"})

        response = communicator.process_operation(mock_call)
        assert response == {"test": "test"}

        # Test for invalid operation
        mock_call = operationExecute(
            operation="invalid operation", deviceName="test", args=None)

        with pytest.raises(Exception):
            communicator.process_operation(mock_call)

        # Test for invalid device
        mock_call = operationExecute(
            operation="mock_process", deviceName="invalid Device", args=None)

        with pytest.raises(Exception):
            communicator.process_operation(mock_call)
