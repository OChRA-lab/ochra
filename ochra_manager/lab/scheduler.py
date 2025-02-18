from ochra_manager.connections.db_connection import DbConnection
from threading import Thread
from ochra_common.utils.enum import OperationStatus


class Scheduler:
    def __init__(self):
        self.schedule = {}
        self.db_conn: DbConnection = DbConnection()
        self._stop = False

    def add_executor(self, station_id):
        self.schedule[station_id] = []

    def remove_executor(self, station_id):
        self.schedule.pop(station_id)

    def add_task(self, station_id, station_client, operation, endpoint):
        self.schedule[station_id].append([station_client, operation, endpoint])

    def run(self):
        self.thread = Thread(target=self.run_loop)
        self.thread.start()

    def run_loop(self):
        while not self._stop:
            for station_id, tasks in self.schedule.items():
                station_client, operation, endpoint = tasks[0]
                # check station status
                station_status = -1

                station_status = self.db_conn.read(
                    {"id": station_id, "_collection": "stations"},
                    "locked",
                )
                if station_status is None or station_status == []:
                    operation.status = OperationStatus.IN_PROGRESS
                    self.db_conn.update(
                        {"id": operation.object_id, "_collection": "operations"},
                        {"status": operation.status},
                    )
                    result = station_client.execute_op(operation, endpoint)
                    operation.status = OperationStatus.COMPLETED
                    self.db_conn.update(
                        {"id": operation.object_id, "_collection": "operations"},
                        {"status": operation.status},
                    )
                    self.db_conn.update(
                        {"id": operation.object_id, "_collection": "operations"},
                        {"result": result.data},
                    )
                    self.schedule[station_id].pop(0)

    def stop(self):
        self._stop = True
        self.thread.join()
