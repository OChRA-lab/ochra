import pytest
from bson import ObjectId
from mongoengine import Document, StringField, disconnect
from ochra_common.connections.db_connection import DbConnection


class TestDocument(Document):
    name = StringField(required=True)
    
@pytest.fixture(scope="module")
def db_connection():
    # Create and connect to local test database
    db_conn = DbConnection(hostname = "localhost", db_name = "test_db")
    yield db_conn.db_adapter
    # Cleanup and disconnect from test database
    db_conn.db_adapter.delete_database()
    disconnect(alias="test_db")
    
def test_create(db_connection):
    # Test creating a document
    doc = TestDocument(name="test_create_doc")
    inserted_id = db_connection.create({"collection_name": "test_collection"}, document=doc)
    assert isinstance(inserted_id, ObjectId), "The document was not created properly."
    
def test_read(db_connection):
    # Test reading a document
    doc = TestDocument(name="test_read_doc")
    inserted_id = db_connection.create({"collection_name": "test_collection"}, document=doc)
    read_doc = db_connection.read({"collection_name": "test_collection", "id": str(inserted_id)}, "name")
    assert read_doc == "test_read_doc", "The document was not read properly."
    
def test_update(db_connection):
    doc = TestDocument(name="test_update_doc")
    inserted_id = db_connection.create({"collection_name": "test_collection"}, document=doc)
    db_connection.update({"collection_name": "test_collection", "id": str(inserted_id)},
                         {"name": "updated_name"},)
    updated_doc = db_connection.read({"collection_name": "test_collection", "id": str(inserted_id)}, "name")
    assert updated_doc == "updated_name", "The document was not updated properly."
    
def test_delete(db_connection):
    # Test deleting a document
    doc = TestDocument(name="test_delete_doc")
    inserted_id = db_connection.create({"collection_name": "test_collection"}, document=doc)
    db_connection.delete("test_collection", {"_id": inserted_id})
    deleted_doc = db_connection.read({"collection_name": "test_collection", "id": str(inserted_id)}, "name")
    assert deleted_doc is None, "The document was not deleted properly."
