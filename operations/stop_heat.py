from .operation import Operation, Operation_


class StopHeat(Operation):
    """StopHeat operation class
    """

    def __init__(self, **kwargs) -> None:
        """initializes the StopHeat class
        """
        super().__init__(self.__class__, **kwargs)
        
    @staticmethod
    def operation_name():
        return "StopHeat"

class StopHeat_(Operation_):
    """StopHeat operation class
    """

    def __init__(self, name="StopHeat", id=None, **kwargs) -> None:
        """initializes the StopHeat class
        """
        super().__init__(name=name, id=id)
        self._doc.arguments = kwargs
        self._db_conn.update(self._doc.collection_name,
                             self._doc.id,
                             {"arguments": self._doc.arguments})
        
    @staticmethod
    def operation_name():
        return "StopHeat"
    