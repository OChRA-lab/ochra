from ochra_common.base import DataModel


def test_base_model():
    # test construction of the base model
    model = DataModel()

    # test base model attributes
    assert model.cls == "ochra_common.base.DataModel"
    assert model.id is not None

    # test base model methods
    assert (
        model.model_dump_json()
        == f'{{"id":"{model.id}","cls":"ochra_common.base.DataModel"}}'
    )
    assert model.model_dump(mode="json") == {
        "id": str(model.id),
        "cls": "ochra_common.base.DataModel",
    }
    assert model.model_dump() == {
        "id": model.id,
        "cls": "ochra_common.base.DataModel",
    }
