from ochra_common.base import DataModel


def test_base_model():
    # test construction of the base model
    model = DataModel()

    # test base model attributes
    assert model.cls == "DataModel"
    assert model.id is not None

    # test base model methods
    assert (
        model.to_json()
        == f'{{"id":"{model.id}","cls":"DataModel"}}'
    )
    assert model.to_dict() == {
        "id": model.id,
        "cls": "DataModel",
    }
