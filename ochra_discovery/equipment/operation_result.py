from ochra_common.equipment.operation_result import OperationResult
from ochra_common.utils.mixins import RestProxyMixinReadOnly
from uuid import UUID
from typing import Union, Type


class OperationResult(OperationResult, RestProxyMixinReadOnly):
    def __init__(self, id: UUID):
        super().__init__()
        self._mixin_hook(self._endpoint, id)

    def get_file(self, filename: str = None) -> bool:
        """Gets the data from the server and saves it to the filename. If filename is not provided, saves it as the original filename

        Args:
            filename (str): The name the file is to be saved. Does not require file extension to be part of the name

        Returns:
            bool: True if successful
        """
        data = self._lab_conn.get_data("operation_results", self.id)
        if filename == None:
            filename = self._lab_conn.get_property(
                "operation_results", self.id, "data_file_name"
            )
        else:
            filename = (
                filename + "."
                + self._lab_conn.get_property(
                    "operation_results", self.id, "data_file_name"
                ).split(".")[-1]
            )
        with open(filename, "wb") as file:
            file.write(data)
            return True
