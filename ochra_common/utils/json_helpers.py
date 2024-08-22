import json
import uuid
from datetime import datetime
import base64


class CustomJSONEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, uuid.UUID):
            return obj.hex  # Convert UUID to hex string
        elif isinstance(obj, datetime):
            return obj.isoformat()  # Convert datetime to ISO 8601 format
        elif isinstance(obj, bytes):
            # Convert bytes to base64 string
            return base64.b64encode(obj).decode('utf-8')
        elif isinstance(obj, dict) or isinstance(obj, list):
            # Handle lists and dicts recursively
            return json.JSONEncoder.default(self, obj)
        return super().default(obj)


class CustomJSONDecoder(json.JSONDecoder):
    def __init__(self, *args, **kwargs):
        super().__init__(object_hook=self.object_hook, *args, **kwargs)

    def object_hook(self, obj):
        # Traverse through the dict and decode values
        if isinstance(obj, dict):
            return {key: self.decode_value(value) for key, value in obj.items()}
        return obj

    def decode_value(self, value):
        if isinstance(value, dict):
            return self.object_hook(value)  # Recursively decode dicts
        elif isinstance(value, list):
            # Recursively decode lists
            return [self.decode_value(item) for item in value]
        elif isinstance(value, str):
            # Attempt to decode UUID
            try:
                return uuid.UUID(value)
            except ValueError:
                pass
            # Attempt to decode datetime
            try:
                return datetime.fromisoformat(value)
            except ValueError:
                pass
            # Attempt to decode base64-encoded bytes
            try:
                decoded_bytes = base64.b64decode(value)
                return decoded_bytes
            except ValueError:
                pass
        return value
