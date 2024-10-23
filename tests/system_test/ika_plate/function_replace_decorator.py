from ochra_common.connections.lab_connection import LabConnection


def api_call(type):
    def decorator(func):
        def wrapper(*args, **kwargs):
            lab_connection: LabConnection = LabConnection()
            obj = args[0]
            lab_connection.call_on_object(type, obj.id, func.__name__, kwargs)
        return wrapper
    return decorator