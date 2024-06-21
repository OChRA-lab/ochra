from operations.operation import Operation, Operation_
from operations.operationModels import OperationResultDbModel
import cv2
import numpy as np


class Image(Operation):
    """Image operation class

    """

    def __init__(self, **kwargs) -> None:
        """initializes the Image class
        """
        super().__init__(self.__class__, **kwargs)

    @property
    def data(self):
        """
            list[Bytes]: list of images data in bytes
        """
        self._doc.data = self._db_conn.read(
            self._doc.collection_name, self._doc.id, "data")
        if self._doc.data is not None:
            dataList = []
            for i in self._doc.data:
                resultEntry = self._db_conn.read(
                    OperationResultDbModel.collection_name, i)
                dataList.append(self._db_conn.read(
                    OperationResultDbModel.collection_name,
                    resultEntry["data"], file=True))
            return dataList
        else:
            return None

    def save_img(self, path, index=0):
        """saves the image to the specified path

        Args:
            path (str): path to save the image
            index (int, optional): index in data list. Defaults to 0.

        Returns:
            str: path of saved file
        """
        imgData = self.data[index]
        nparr = np.frombuffer(imgData, np.uint8)
        img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
        cv2.imwrite("image.png", img)
        return path


class Image_(Operation_):
    """Image operation class

    """

    def __init__(self, name="Image", id=None, **kwargs) -> None:
        """initializes the Image class

        Args:
            name (str, optional): name of operation. Defaults to "Image".
            id (ObjectId, optional): id to load operation from db.
                                    Defaults to None.
        """
        super().__init__(name=name, id=id)
        self._doc.arguments = kwargs
        self._db_conn.update(self._doc.collection_name, self._doc.id,
                             {"arguments": self._doc.arguments})

    @property
    def data(self):
        """
            list[Bytes]: list of images data in bytes
        """
        self._doc.data = self._db_conn.read(
            self._doc.collection_name, self._doc.id, "data")
        return self._doc.data
