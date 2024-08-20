from OChRA_Common.ochra_common.spaces.work_station import WorkStation as WorkStationAbstract
from ochra_common.utils.db_decorator import middle_db


@middle_db
class WorkStation(WorkStationAbstract):
    def add_device(self, device):
        self.devices.append(device)

    def remove_device(self, device):
        self.devices.remove(device)
