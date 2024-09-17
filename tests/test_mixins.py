import pytest
from unittest.mock import MagicMock, patch
from uuid import UUID, uuid4
from pydantic import BaseModel, Field
from ochra_common.utils.mixins import RestProxyMixin, RestProxyMixinReadOnly

class TestDataModel(BaseModel, RestProxyMixin):
    id: UUID = Field(default_factory=uuid4)
    cls: str = Field(default=None)
    params: dict = Field(default=None)

@patch("ochra_common.utils.mixins.LabConnection")
def test_rest_proxy_mixin(MockLabConnection):
    mock_lab_conn = MockLabConnection.return_value
    mock_lab_conn.get_property.return_value = 'mock_value'

    test_model = TestDataModel(cls="test_cls", params={"param": "value"})
    
    test_model._mixin_hook("test_type", test_model.id)

    assert test_model.cls == 'mock_value'
    mock_lab_conn.get_property.assert_called_once_with('test_type', test_model._lab_conn.get_object_by_name.return_value.id, 'cls')

def test_rest_proxy_mixin_read_only():
    pass