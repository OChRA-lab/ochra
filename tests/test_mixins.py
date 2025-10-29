import pytest
from unittest.mock import patch
from uuid import UUID, uuid4
from pydantic import BaseModel, Field
from ochra_common.utils.mixins import RestProxyMixin, RestProxyMixinReadOnly


class DataModel(BaseModel):
    id: UUID = Field(default_factory=uuid4)
    cls: str = Field(default=None)

    def model_post_init(self, __context) -> None:
        self.cls = f"{self.__class__.__module__}.{self.__class__.__name__}"
        return super().model_post_init(__context)


class TestModel(DataModel):
    _endpoint = "/test/endpoint"

    name: str = Field(default=None)
    params: dict


class TestModelProxy(TestModel, RestProxyMixin):
    def __init__(self, object_id, name, params):
        super().__init__(id=object_id, name=name, params=params)
        self._mixin_hook(self._endpoint, object_id)


class TestModelReadOnlyProxy(TestModel, RestProxyMixinReadOnly):
    def __init__(self, name, **params):
        super().__init__()
        self._mixin_hook(self._endpoint, name)


@patch("ochra_common.utils.mixins.LabConnection")
def test_rest_proxy_mixin(MockLabConnection):
    object_id = uuid4()
    test_model = TestModelProxy(object_id, name="test_name", params={"param": "value"})

    # to get the instance of the used mock inside TestData
    mock_lab_connection = MockLabConnection.return_value

    # test construction
    mock_lab_connection.construct_object.assert_called_with(
        "/test/endpoint", test_model
    )

    # test getter
    test_model.name
    mock_lab_connection.get_property.assert_called_with(
        "/test/endpoint", object_id, "name"
    )

    # test ignored fields [id, cls]
    mock_lab_connection.get_property.reset_mock()  # reset call count
    assert object_id == test_model.id
    mock_lab_connection.get_property.assert_not_called()

    assert (
        test_model.cls
        == f"{test_model.__class__.__module__}.{
        test_model.__class__.__name__}"
    )
    mock_lab_connection.get_property.assert_not_called()

    # test setter
    test_model.name = "new_value"
    mock_lab_connection.set_property.assert_called_with(
        "/test/endpoint", object_id, "name", "new_value"
    )


@patch("ochra_common.utils.mixins.LabConnection")
def test_rest_proxy_mixin_read_only(MockLabConnection):
    mock_lab_connection = MockLabConnection.return_value
    id = uuid4()
    mock_lab_connection.get_object_id.return_value = id
    mock_lab_connection.get_property.return_value = "test_mixins.TestModelReadOnlyProxy"
    name = "unique_name"
    test_model = TestModelReadOnlyProxy(name=name, params={"param": "value"})

    # test object retrieval
    mock_lab_connection.get_object_id.assert_called_with("/test/endpoint", name)
    mock_lab_connection.get_property.assert_called_with("/test/endpoint", id, "cls")

    # test getter
    test_model.name
    mock_lab_connection.get_property.assert_called_with("/test/endpoint", id, "name")

    # test ignored fields [id, cls]
    mock_lab_connection.get_property.reset_mock()  # reset call count
    assert test_model.id != None
    mock_lab_connection.get_property.assert_not_called()

    assert (
        test_model.cls
        == f"{test_model.__class__.__module__}.{
        test_model.__class__.__name__}"
    )
    mock_lab_connection.get_property.assert_not_called()

    # test setter
    test_model.name = "new_value"
    mock_lab_connection.set_property.assert_not_called()


@patch("ochra_common.utils.mixins.LabConnection")
def test_read_only_from_id(MockLabConnection):
    mock_lab_connection = MockLabConnection.return_value
    id = uuid4()
    name = "test_name"
    cls = "test_mixins.TestModelReadOnlyProxy"
    params = {"test_params": "test_args"}

    # mock_lab_connection.get_property.side_effect = [
    #     name, id, cls, params, name, params, params]
    mock_lab_connection.get_property.side_effect = [cls, name, params, params]
    test_instance = TestModelReadOnlyProxy.from_id(id)

    # test instance is created
    assert isinstance(test_instance, TestModelReadOnlyProxy)

    # test getters properly set
    assert test_instance.name == name
    mock_lab_connection.get_property.assert_called_with("/test/endpoint", id, "name")
    assert test_instance.params == params
    mock_lab_connection.get_property.assert_called_with("/test/endpoint", id, "params")

    # test setters are ignored
    test_instance.params = {"new_params": "new_args"}
    mock_lab_connection.set_property.assert_not_called()
    assert test_instance.params == params
    mock_lab_connection.get_property.assert_called_with("/test/endpoint", id, "params")

    # test ignored fields [id, cls]
    mock_lab_connection.get_property.reset_mock()  # reset call count
    assert test_instance.id != None
    mock_lab_connection.get_property.assert_not_called()

    assert (
        test_instance.cls
        == f"{test_instance.__class__.__module__}.{
        test_instance.__class__.__name__}"
    )
    mock_lab_connection.get_property.assert_not_called()


@patch("ochra_common.utils.mixins.LabConnection")
def test_proxy_from_id(MockLabConnection):
    mock_lab_connection = MockLabConnection.return_value
    id = uuid4()
    name = "test_name"
    params = {"test_params": "test_args"}

    mock_lab_connection.get_property.side_effect = [
        id,
        name,
        params,
        name,
        params,
        "new_name",
    ]
    test_instance = TestModelProxy.from_id(id)

    # test instance is created
    assert isinstance(test_instance, TestModelProxy)

    # test getters properly set
    assert test_instance.name == name
    mock_lab_connection.get_property.assert_called_with("/test/endpoint", id, "name")
    assert test_instance.params == params
    mock_lab_connection.get_property.assert_called_with("/test/endpoint", id, "params")

    # test setters
    test_instance.name = "new_name"
    mock_lab_connection.set_property.assert_called_with(
        "/test/endpoint", id, "name", "new_name"
    )
    assert test_instance.name == "new_name"
    mock_lab_connection.get_property.assert_called_with("/test/endpoint", id, "name")

    # test ignored fields [id, cls]
    mock_lab_connection.get_property.reset_mock()  # reset call count
    assert test_instance.id != None
    mock_lab_connection.get_property.assert_not_called()

    assert (
        test_instance.cls
        == f"{test_instance.__class__.__module__}.{
        test_instance.__class__.__name__}"
    )
    mock_lab_connection.get_property.assert_not_called()
