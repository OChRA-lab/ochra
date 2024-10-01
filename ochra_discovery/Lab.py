from ochra_common.spaces.lab import Lab
from ochra_common.connections.lab_connection import LabConnection
from ochra_common.utils.mixins import RestProxyMixinReadOnly


class Lab(Lab, RestProxyMixinReadOnly):

    def __init__() -> None:
        super().__init__()
        self._lab_conn = LabConnection()
        self._lab_conn.construct_object("lab", self)