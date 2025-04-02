from uuid import UUID
from typing import Dict, Any
from ..base import DataModel


def is_valid_uuid(string: str) -> bool:
    """Check if a string is a valid UUID.

    Args:
        string (str): The string to check.

    Returns:
        bool: True if the string is a valid UUID, False otherwise.
    """
    try:
        UUID(string)
        return True
    except ValueError:
        return False

def is_data_model(obj: Any) -> bool:
    """Check if an dict is a DataModel.

    Args:
        obj (Any): The object to check.

    Returns:
        bool: True if the object is a DataModel, False otherwise.
    """
    if isinstance(obj, dict) and all(key in obj for key in ["id", "cls", "collection", "module_path"]):
        return True
    else:
        return False

def convert_to_data_model(a_dict: Dict) -> DataModel:
    """Convert a dict to a DataModel.

    Args:
        a_dict (Dict): The dict to convert.

    Returns:
        DataModel: The converted DataModel.
    """
    return DataModel(
        id=a_dict["id"],
        cls=a_dict["cls"],
        collection=a_dict["collection"],
        module_path=a_dict["module_path"],
    )