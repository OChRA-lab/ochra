import pytest
from unittest.mock import MagicMock
from src.OChRA_Common.connections.db_connection import DbConnection


@pytest.fixture
def db_connection():
    # Mock the MongoDbAdapter used in DbConnection
    with pytest.MonkeyPatch.context() as m:
        mock_adapter = MagicMock()
        m.setattr("OChRA_Common.connections.mongo_adapter.MongoDbAdapter",
                  lambda *args, **kwargs: mock_adapter)
        # Create an instance of DbConnection with the mocked adapter
        db_conn = DbConnection(hostname="test_host", db_name="test_db")
    return db_conn, mock_adapter


def test_create(db_connection):
    db_conn, mock_adapter = db_connection
    mock_adapter.create.return_value = "mocked_create_result"
    result = db_conn.create("test_collection", {"key": "value"})
    mock_adapter.create.assert_called_once_with(
        "test_collection", {"key": "value"})
    assert result == "mocked_create_result"


def test_read(db_connection):
    db_conn, mock_adapter = db_connection
    mock_adapter.read.return_value = "mocked_read_result"
    result = db_conn.read("test_collection", "test_id")
    mock_adapter.read.assert_called_once_with(
        "test_collection", "test_id", None, file=False)
    assert result == "mocked_read_result"


def test_update(db_connection):
    db_conn, mock_adapter = db_connection
    mock_adapter.update.return_value = "mocked_update_result"
    result = db_conn.update("test_collection", "test_id", {
                            "$set": {"key": "new_value"}})
    mock_adapter.update.assert_called_once_with(
        "test_collection", "test_id", {"$set": {"key": "new_value"}})
    assert result == "mocked_update_result"


def test_delete(db_connection):
    db_conn, mock_adapter = db_connection
    mock_adapter.delete.return_value = "mocked_delete_result"
    result = db_conn.delete("test_collection", "test_id")
    mock_adapter.delete.assert_called_once_with("test_collection", "test_id")
    assert result == "mocked_delete_result"
