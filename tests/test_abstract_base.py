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
