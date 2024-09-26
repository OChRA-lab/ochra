import pytest
from unittest.mock import patch
from uuid import UUID, uuid4
from pydantic import BaseModel, Field
from ochra_common.utils.mixins import RestProxyMixin, RestProxyMixinReadOnly
from collections import namedtuple


class TestDataModel(BaseModel):
    id: UUID = Field(default_factory=uuid4)
    name: str = Field(default=None)
    params: dict = Field(default=None)


class TestData(TestDataModel, RestProxyMixin):
    def __init__(self, object_id, **params):
        super().__init__(id=object_id, name=self.__class__.__name__, params=params)
        self._mixin_hook("/test/endpoint", object_id)


class TestDataReadOnly(TestDataModel, RestProxyMixinReadOnly):
    def __init__(self, name, **params):
        super().__init__(id=uuid4(), name=name, params=params)
        self._mixin_hook("/test/endpoint", name)


@patch("ochra_common.utils.mixins.LabConnection")
def test_rest_proxy_mixin(MockLabConnection):

    object_id = uuid4()
    test_model = TestData(object_id, params={"param": "value"})

    # to get the instance of the used mock inside TestData
    mock_lab_connection = MockLabConnection.return_value

    # test construction
    mock_lab_connection.construct_object.assert_called_with(
        "/test/endpoint", test_model)

    # test getter
    test_model.name
    mock_lab_connection.get_property.assert_called_with(
        "/test/endpoint", object_id, 'name')

    # test setter
    test_model.name = 'new_value'
    mock_lab_connection.set_property.assert_called_with(
        "/test/endpoint", object_id, 'name', 'new_value')


@ patch("ochra_common.utils.mixins.LabConnection")
def test_rest_proxy_mixin_read_only(MockLabConnection):
    mock_lab_connection = MockLabConnection.return_value
    Response = namedtuple('Response', ['id'])
    res = Response(id=uuid4())
    mock_lab_connection.get_object.return_value = res

    name = "unique_name"
    test_model = TestDataReadOnly(
        name=name, params={"param": "value"})

    # test object retrieval
    mock_lab_connection.get_object.assert_called_with(
        "/test/endpoint", name)

    # test getter
    test_model.name
    mock_lab_connection.get_property.assert_called_with(
        "/test/endpoint", res.id, 'name')

    # test setter
    test_model.name = 'new_value'
    mock_lab_connection.set_property.assert_not_called()
