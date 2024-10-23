import pytest
from bson import ObjectId
from ochra_manager.connections.db_connection import DbConnection
from uuid import UUID
from pydantic import BaseModel


class TestDocument(BaseModel):
    name: str
    id: str

    def to_json(self):
        return self.model_dump_json()


@pytest.fixture(scope="module")
def db_connection():
    # Create and connect to local test database
    db_conn = DbConnection(hostname="localhost:27017", db_name="test_db")
    yield db_conn.db_adapter
    # Delete and disconnect from test database
    db_conn.db_adapter.delete_database()


@pytest.fixture(scope="module")
def test_data():
    # Collection and document to be used in tests
    test_coll = {"_collection": "test_collection"}
    test_doc = TestDocument(name="test_doc", id="test_id")
    return test_coll, test_doc


def test_create(db_connection, test_data):
    # Test creating a document
    doc_to_create = db_connection.create(test_data[0], test_data[1])
    assert isinstance(
        doc_to_create, ObjectId), "The document was not created properly."


def test_read(db_connection, test_data):
    # Test reading a document
    doc_to_read = db_connection.create(test_data[0], test_data[1])
    read_doc = db_connection.read(
        {"_collection": "test_collection", "id": test_data[1].id}, "name")
    assert read_doc == "test_doc", "The document was not read properly."


def test_update(db_connection, test_data):
    # Test updating a document
    doc_to_update = db_connection.create(test_data[0], test_data[1])
    db_connection.update({"_collection": "test_collection", "id": test_data[1].id},
                         {"name": "updated_name"},)
    updated_doc = db_connection.read(
        {"_collection": "test_collection", "id": test_data[1].id}, "name")
    assert updated_doc == "updated_name", "The document was not updated properly."


def test_delete(db_connection, test_data):
    # Test deleting a document
    doc_to_delete = db_connection.create(test_data[0], test_data[1])
    db_connection.delete("test_collection", {"_id": doc_to_delete})
    deleted_doc = db_connection.read(
        {"_collection": "test_collection", "id": test_data[1].id}, "name")
    assert deleted_doc is None, "The document was not deleted properly."

def test_find(db_connection, test_data):
    # Test finding a document
    test_doc_1 = TestDocument(name="test_doc", id="123")
    test_doc_2 = TestDocument(name="test_doc", id="456")
    db_connection.create(test_data[0], test_doc_1)
    db_connection.create(test_data[0], test_doc_2)
    found_doc = db_connection.find(
        {"_collection": "test_collection"}, {"name": "test_doc"})
    assert found_doc["name"] == "test_doc", "The document was not found properly."

def test_find_all(db_connection, test_data):
    # Test finding all documents
    test_doc_1 = TestDocument(name="test_doc", id="123")
    test_doc_2 = TestDocument(name="test_doc", id="456")
    db_connection.create(test_data[0], test_doc_1)
    db_connection.create(test_data[0], test_doc_2)
    found_docs = db_connection.find_all(
        {"_collection": "test_collection"}, {"name": "test_doc"})
    assert len(found_docs) == 2, "The documents were not found properly."
    assert found_docs[0]["name"] == "test_doc", "The document was not found properly."
    assert found_docs[1]["name"] == "test_doc", "The document was not found properly."
    assert found_docs[0]["id"] != found_docs[1]["id"]
