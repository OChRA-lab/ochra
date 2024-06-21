from operations.operation import Operation, Operation_


class Dispense(Operation):
    """Dispense operation class

    """

    def __init__(self, volume, source, dest, direction, **kwargs) -> None:
        """initializes the Dispense class

        Args:
            volume (int): volume to dispense µl
            source (int): source port on pump
            dest (int): dest port on pump
            direction (str): direction to spin pump valve I for clockwise
                            and O for counter clockwise
        """
        super().__init__(self.__class__, volume=volume,
                         source=source,
                         dest=dest,
                         direction=direction,
                         **kwargs,)


class Dispense_(Operation_):
    """Dispense operation class

    """

    def __init__(self, volume, source, dest, direction,
                 name="Dispense", id=None, **kwargs) -> None:
        """initializes the Dispense class

        Args:
            volume (int): volume to dispense µl
            source (int): source port on pump
            dest (int): dest port on pump
            direction (str): direction to spin pump valve I for clockwise
                            and O for counter clockwise
            name (str, optional): name of operation. Defaults to "Dispense".
            id (ObjectId, optional): id to load operation from db.
                                    Defaults to None.
        """
        super().__init__(name=name, id=id)
        self._doc.arguments = kwargs
        self._doc.arguments["volume"] = volume
        self._doc.arguments["source"] = source
        self._doc.arguments["dest"] = dest
        self._doc.arguments["direction"] = direction
        self._db_conn.update(self._doc.collection_name,
                             self._doc.id,
                             {"arguments": self._doc.arguments})
