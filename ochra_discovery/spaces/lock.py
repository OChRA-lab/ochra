from ochra_common.spaces.station import Station

class Lock(object):
    def __init__(self, station: Station):
        self.station = station
        self.station.lock()
    def __enter__(self):
        return self.station
    def __exit__(self, exc_type, exc_value, traceback):
        self.station.unlock()