from ochra_common.connections.lab_connection import LabConnection
from ochra_common.spaces.station import Station

class Lock(object):
    def __init__(self, station: Station):
        self._lab_conn: LabConnection = LabConnection()
        self.station = station
        self.station.lock(self._lab_conn._session_id)
    def __enter__(self):
        return self.station
    def __exit__(self, exc_type, exc_value, traceback):
        self.station.unlock(self._lab_conn._session_id)