import pytest
from bson import ObjectId
from mongoengine import Document, StringField, disconnect
from ochra_common.connections.db_connection import DbConnection

class TestDocument(Document):
    name = StringField(required=True)
    
@pytest.fixture(scope="module")
def db_connection():
    db_conn = DbConnection(hostname = "localhost", db_name = "test_db")
    yield db_conn.db_adapter
    db_conn.db_adapter.delete_database()
    disconnect(alias="test_db")
    
def test_create(db_connection):
    doc = TestDocument(name="test_create_doc")
    inserted_id = db_connection.create({"collection_name": "test_collection"}, document=doc)
    assert isinstance(inserted_id, ObjectId), "The document was not created properly."
    