from ochra_common.base import DataModel


def test_base_model():
    # test construction of the base model
    model = DataModel()

    # test base model attributes
    assert model.cls == "DataModel"
    assert model.id is not None

    # test base model methods
    assert (
        model.model_dump_json()
        == f'{{"id":"{model.id}","collection":null,"cls":"DataModel","module_path":null}}'
    )
    assert model.model_dump(mode="json") == {
        "id": str(model.id),
        "collection": None,
        "cls": "DataModel",
        "module_path": None,
    }
    assert model.model_dump() == {
        "id": model.id,
        "collection": None,
        "cls": "DataModel",
        "module_path": None,
    }

def test_get_base_model():
    # test construction of the base model
    model = DataModel(collection="test_col", module_path="test_module")

    # test get_base_model method
    base_model = model.get_base_model()
    assert base_model.id == model.id
    assert base_model.collection == model.collection
    assert base_model.cls == model.cls
    assert base_model.module_path == model.module_path
