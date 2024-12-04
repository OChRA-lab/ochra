from uuid import UUID


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
