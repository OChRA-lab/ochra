from .operation import Operation, Operation_


class StartStir(Operation):
    """StartStir operation class
    """

    def __init__(self, speed, **kwargs) -> None:
        """initializes the StartStir class

        Args:
            speed (int): speed of stirrer
        """
        super().__init__(self.__class__, speed=speed, **kwargs)

    @property
    def speed(self):
        """
            int: speed of stirrer
        """
        return self._doc.arguments["speed"]
    
    @staticmethod
    def operation_name():
        return "StartStir"


class StartStir_(Operation_):
    """StartStir operation class
    """

    def __init__(self, name="StartStir", id=None, **kwargs) -> None:
        """initializes the StartStir class

        Args:
            speed (int): speed of stirrer
        """
        super().__init__(name=name, id=id)
        self._doc.arguments = kwargs
        self._db_conn.update(self._doc.collection_name,
                             self._doc.id,
                             {"arguments": self._doc.arguments})

    @property
    def speed(self):
        """
            int: speed of stirrer
        """
        return self._doc.arguments["speed"]
    
    @staticmethod
    def operation_name():
        return "StartStir"
    