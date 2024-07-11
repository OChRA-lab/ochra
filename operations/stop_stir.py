from .operation import Operation, Operation_


class StopStir(Operation):
    """StopStir operation class
    """

    def __init__(self, **kwargs) -> None:
        """initializes the StopStir class
        """
        super().__init__(self.__class__, **kwargs)
    @staticmethod
    def name(self):
        return "StopStir"

class StopStir_(Operation_):
    """StopStir operation class
    """

    def __init__(self, name="StopStir", id=None, **kwargs) -> None:
        """initializes the StopStir class
        """
        super().__init__(name=name, id=id)
        self._doc.arguments = kwargs
        self._db_conn.update(self._doc.collection_name,
                             self._doc.id,
                             {"arguments": self._doc.arguments})
    @staticmethod
    def name(self):
        return "StopStir"