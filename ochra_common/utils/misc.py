from uuid import UUID

def is_valid_uuid(string: str) -> bool:
    try:
        UUID(string)
        return True
    except ValueError:
        return False