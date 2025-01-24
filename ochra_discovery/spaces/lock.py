from contextlib import contextmanager

@contextmanager
def lock(station):
    station.lock()
    try:
        yield station
    finally:
        station.unlock()

class Lock(object):
    def __init__(self, station):
        self.station = station
        self.station.lock()
    def __enter__(self):
        return self.station
    def __exit__(self, exc_type, exc_value, traceback):
        self.station.unlock()