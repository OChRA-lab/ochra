from .operation import Operation, Operation_


class RobotTask(Operation):
    """RobotTask operation class
    """

    def __init__(self, robot_op, **kwargs) -> None:
        """initializes the RobotTask class

        Args:
            robot_op (str): robot operation to perform
        """
        super().__init__(self.__class__, robot_op=robot_op, **kwargs)

    @property
    def robot_op(self):
        return self._doc.arguments["robot_op"]


class RobotTask_(Operation_):
    """RobotTask operation class
    """

    def __init__(self, robot_op, id=None, **kwargs) -> None:
        """initializes the RobotTask class

        Args:
            robot_op (str): robot operation to perform
            id (ObjectId, optional): objectid of operation to load from db.
                                    Defaults to None.
        """
        super().__init__(name=robot_op, id=id)
        self._doc.arguments = kwargs
        self._doc.arguments["robot_op"] = robot_op
        self._db_conn.update(self._doc.collection_name, self._doc.id,
                             {"arguments": self._doc.arguments})

    @property
    def robot_op(self):
        return self._doc.arguments["robot_op"]
