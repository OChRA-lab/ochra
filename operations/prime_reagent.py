from .operation import Operation, Operation_


class PrimeReagent(Operation):
    """PrimeReagent operation class

    """

    def __init__(self, source, volume, **kwargs) -> None:
        """initializes the PrimeReagent class

        Args:
            source (int): source port on pump
            volume (int): volume to dispense µl
        """
        super().__init__(self.__class__, source=source, 
                         volume=volume, 
                         **kwargs,)
        
    @staticmethod
    def operation_name():
        return "PrimeReagent"


class PrimeReagent_(Operation_):
    """PrimeReagent operation class

    """

    def __init__(self, source, volume,
                 name="PrimeReagent", id=None, **kwargs) -> None:
        """initializes the PrimeReagent class

        Args:
            source (int): source port on pump
            volume (int): volume to dispense µl
            name (str, optional): name of operation. Defaults to "PrimeReagent".
            id (ObjectId, optional): id to load operation from db.
                                    Defaults to None.
        """
        super().__init__(name=name, id=id)
        self._doc.arguments = kwargs
        self._doc.arguments["source"] = source
        self._doc.arguments["volume"] = volume
        self._db_conn.update(self._doc.collection_name,
                             self._doc.id,
                             {"arguments": self._doc.arguments})
    
    @staticmethod
    def operation_name():
        return "PrimeReagent"
