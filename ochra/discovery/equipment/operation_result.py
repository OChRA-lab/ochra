from ochra.common.equipment.operation_result import OperationResult
from ochra.common.utils.mixins import RestProxyMixinReadOnly
from uuid import UUID
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

    def save_data(self, path: str = None) -> bool:
        """
        Gets the data from the server and saves it to path. If path is not provided,
        saves it using the original name at the current directory

        Args:
            path (str): The path to save the data to. If None, saves it to the current directory using original name.

        Returns:
            bool: True if the data is saved.
        """
        data = self._lab_conn.get_data("operation_results", self.id)
        if path is None:
            path = self._lab_conn.get_property(
                "operation_results", self.id, "data_file_name"
            )
        else:
            path = (
                path + "."
                + self._lab_conn.get_property(
                    "operation_results", self.id, "data_file_name"
                ).split(".")[-1]
            )
        with open(path, "wb") as file:
            file.write(data)
        
        if self._lab_conn.get_property(
            "operation_results", self.id, "data_type"
        ) == "folder":
            shutil.unpack_archive(path, path.split(".")[0], "zip")
            remove(path)

        return True
