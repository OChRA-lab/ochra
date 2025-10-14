from threading import Lock
from typing import Any


class SingletonMeta(type):
    """Thread-safe Singleton metaclass.

    Ensures that only one instance of a class exists,
    even in multi-threaded environments.
    """

    _instances = {}

    _lock: Lock = Lock()

    def __call__(self, *args: Any, **kwds: Any) -> Any:
        """
        create an instance of singleton if one exists return that instance

        Returns:
            Any: singleton instance
        """
        with self._lock:
            if self not in self._instances:
                instance = super().__call__(*args, **kwds)
                self._instances[self] = instance
        return self._instances[self]
