from ochra_manager.connections.db_connection import DbConnection
from ochra_common.equipment.operation import Operation
from threading import Thread
from time import sleep
from ochra_common.utils.enum import ActivityStatus
from fastapi import HTTPException
from ..connections.station_connection import StationConnection


class Scheduler:
    def __init__(self):
        self.op_queue = []
        self._db_conn: DbConnection = DbConnection()
        self._stop = False

        # create operation queue in db
        self._queue_id = self._db_conn.create(
            {"_collection": "lab"}, {"op_queue": self.op_queue}
        )

    def add_operation(self, operation: Operation, collection: str):
        self.op_queue.append((operation, collection))

    def run(self):
        self.thread = Thread(target=self._schedule, daemon=False)
        self.thread.start()

    def _schedule(self):
        while not self._stop:
            queue = self.op_queue.copy()
            for operation, collection in queue:
                # resolve station id and endpoint
                station_id, endpoint = self._resolve_station_id_endpoint(
                    str(operation.entity_id), collection
                )

                # check station status
                station_status = self._db_conn.read(
                    {"id": station_id, "_collection": "stations"},
                    "status",
                )

                if station_status == ActivityStatus.IDLE:
                    # check if station is locked by a user
                    station_locked_by = self._db_conn.read(
                        {"id": station_id, "_collection": "stations"},
                        "locked",
                    )

                    if not station_locked_by or station_locked_by == str(
                        operation.caller_id
                    ):
                        # remove operation from queue
                        self.op_queue.remove((operation, collection))

                        # execute operation in a new daemon thread
                        op_thread = Thread(
                            target=self._execute_op,
                            args=(operation, station_id, endpoint),
                            daemon=True,
                        )
                        op_thread.start()
                        sleep(1)  # needed to allow the station to update its status
            # update queue in db and sleep
            if queue != self.op_queue:
                self._db_conn.update(
                    {"id": self._queue_id, "_collection": "lab"},
                    {
                        "op_queue": [
                            op.get_base_model().model_dump_json()
                            for op, _ in self.op_queue
                        ]
                    },
                )
            sleep(1)

    def stop(self):
        self._stop = True
        self.thread.join()

    def _execute_op(self, operation, station_id, endpoint):
        # establish connection with station
        station_ip = self._db_conn.read(
            {"id": station_id, "_collection": "stations"}, "station_ip"
        )

        station_port = self._db_conn.read(
            {"id": station_id, "_collection": "stations"}, "port"
        )
        station_client: StationConnection = StationConnection(
            station_ip + ":" + str(station_port)
        )
        # execute operation and save result in db
        result = station_client.execute_op(operation, endpoint)
        self._db_conn.update(
            {"id": operation.id, "_collection": "operations"},
            {"result": result.data},
        )

    def _resolve_station_id_endpoint(self, target_entity_id: str, collection: str):
        if collection == "devices" or collection == "robots":
            station_id = self._db_conn.read(
                {"id": target_entity_id, "_collection": collection}, "owner_station"
            )
            if station_id is None:
                raise HTTPException(status_code=404, detail="station not found")
            endpoint = (
                "process_device_op" if collection == "devices" else "process_robot_op"
            )
        else:
            station_id = target_entity_id
            endpoint = "process_station_op"
        return station_id, endpoint
