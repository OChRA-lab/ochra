from threading import Lock, Thread
from typing import Any


class SingletonMeta(type):
    """
    ThreadSafe Singleton
    """
    _instances = {}

    _lock: Lock = Lock()

    def __call__(self, *args: Any, **kwds: Any) -> Any:
        """create an instance of singleton if one exists return that

        Returns:
            Any: singleton instance
        """
        with self._lock:
            if self not in self._instances:
                instance = super().__call__(*args, **kwds)
                self._instances[self] = instance
        return self._instances[self]
