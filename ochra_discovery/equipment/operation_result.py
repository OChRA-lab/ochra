from ochra_common.equipment.operation_result import OperationResult
from ochra_common.utils.mixins import RestProxyMixinReadOnly
from uuid import UUID
from typing import Union, Type
import shutil
from os import remove

class OperationResult(OperationResult, RestProxyMixinReadOnly):
    def __init__(self, id: UUID):
        """Operation Result object

        Args:
            id (UUID): The id of the operation result
        """
        super().__init__()
        self._mixin_hook(self._endpoint, id)

    def save_data(self, name: str = None) -> bool:
        """Gets the data from the server and saves it to name. If name is not provided, saves it as the original name

        Args:
            name (str): The name the file is to be saved. Does not require file extension to be part of the name

        Returns:
            bool: True if successful
        """
        data = self._lab_conn.get_data("operation_results", self.id)
        if name == None:
            name = self._lab_conn.get_property(
                "operation_results", self.id, "data_file_name"
            )
        else:
            name = (
                name + "."
                + self._lab_conn.get_property(
                    "operation_results", self.id, "data_file_name"
                ).split(".")[-1]
            )
        with open(name, "wb") as file:
            file.write(data)
        
        if self._lab_conn.get_property(
            "operation_results", self.id, "data_type"
        ) == "folder":
            shutil.unpack_archive(name, name.split(".")[0], "zip")
            remove(name)

        return True
