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
    