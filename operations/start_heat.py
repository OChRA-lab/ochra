from .operation import Operation, Operation_


class StartHeat(Operation):
    """StartHeat operation class
    """

    def __init__(self, temperature, **kwargs) -> None:
        """initializes the StartHeat class

        Args:
            temperature (int): temperature of plate
        """
        super().__init__(self.__class__, temperature=temperature, **kwargs)

    @property
    def temperature(self):
        """
            int: temperature of plate
        """
        return self._doc.arguments["temperature"]
    
    @staticmethod
    def operation_name():
        return "StartHeat"


class StartHeat(Operation_):
    """StartHeat operation class
    """

    def __init__(self, name="StartHeat", id=None, **kwargs) -> None:
        """initializes the StartHeat class

        Args:
            temperature (int): temperature of stirrer
        """
        super().__init__(name=name, id=id)
        self._doc.arguments = kwargs
        self._db_conn.update(self._doc.collection_name,
                             self._doc.id,
                             {"arguments": self._doc.arguments})

    @property
    def temperature(self):
        """
            int: temperature of plate
        """
        return self._doc.arguments["temperature"]
    
    @staticmethod
    def operation_name():
        return "StartHeat"
    