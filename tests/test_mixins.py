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
    id = test_model.id

    test_model._mixin_hook("test_type", test_model.id)

    # test getter
    assert test_model.cls == 'mock_value'
    mock_lab_conn.get_property.assert_called_with('test_type', id, 'cls')

    # test setter
    test_model.cls = 'new_value'
    mock_lab_conn.set_property.assert_called_with(
        'test_type', id, 'cls', 'new_value')


class TestDataModelReadOnly(BaseModel, RestProxyMixinReadOnly):
    id: UUID = Field(default_factory=uuid4)
    cls: str = Field(default=None)
    params: dict = Field(default=None)


@patch("ochra_common.utils.mixins.LabConnection")
def test_rest_proxy_mixin_read_only(MockLabConnection):
    mock_lab_conn = MockLabConnection.return_value
    mock_lab_conn.get_property.return_value = 'mock_value'

    test_model = TestDataModelReadOnly(
        cls="test_cls", params={"param": "value"})
    id = test_model.id
    mock_lab_conn.get_object_by_name.return_value.id = id

    test_model._mixin_hook("test_type", "myName")

    # test getter
    assert test_model.cls == 'mock_value'
    mock_lab_conn.get_property.assert_called_with('test_type', id, 'cls')

    # test setter
    test_model.cls = 'new_value'
    assert test_model.cls == 'mock_value'
