from ochra_manager.connections.db_connection import DbConnection
from ochra_common.equipment.operation import Operation
from threading import Thread
from time import sleep
from ochra_common.utils.enum import ActivityStatus, PatchType
from fastapi import HTTPException
from ..connections.station_connection import StationConnection
import logging


class Scheduler:
    def __init__(self):
        self.op_queue = []
        self._db_conn: DbConnection = DbConnection()
        self._stop = False
        self._logger = logging.getLogger(__name__)
        self._logger.info("Test message")

        # create operation queue in db
        self._queue_id = self._db_conn.create(
            {"_collection": "lab"}, {"op_queue": self.op_queue}
        )

    def add_operation(self, operation: Operation):
        self.op_queue.append(operation)

    def run(self):
        self.thread = Thread(target=self._schedule, daemon=False)
        self.thread.start()

    def _schedule(self):
        while not self._stop:
            queue = self.op_queue.copy()
            for operation in queue:
                # resolve station id and endpoint
                station_id = self._resolve_station_id(operation)

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
                        self.op_queue.remove(operation)

                        # execute operation in a new daemon thread
                        op_thread = Thread(
                            target=self._execute_op,
                            args=(operation, station_id),
                            daemon=True,
                        )
                        op_thread.start()
                        sleep(1)  # needed to allow the station to update its status
            # update queue in db and sleep
            if queue != self.op_queue:
                self._db_conn.update(
                    {"id": self._queue_id, "_collection": "lab"},
                    {
                        "property": "op_queue",
                        "property_value": [
                            op.get_base_model().model_dump_json()
                            for op in self.op_queue
                        ],
                        "patch_type": PatchType.SET,
                        "patch_args": None,
                    },
                )
            sleep(1)

    def stop(self):
        self._stop = True
        self.thread.join()

    def _execute_op(self, operation, station_id):
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
        # TODO fix this when working on operation handling issue
        result = station_client.execute_op(operation, "process_op")
        self._db_conn.update(
            {"id": operation.id, "_collection": "operations"},
            {
                "property": "result",
                "property_value": result.data,
                "patch_type": PatchType.SET,
                "patch_args": None,
            },
        )

    def _resolve_station_id(self, op: Operation):
        target_entity_id = str(op.entity_id)
        target_entity_type = op.entity_type
        if target_entity_type == "device" or target_entity_type == "robot":
            station_id = self._db_conn.read(
                {
                    "id": target_entity_id,
                    "_collection": "devices"
                    if target_entity_type == "device"
                    else "robots",
                },
                "owner_station",
            )
            if station_id is None:
                raise HTTPException(status_code=404, detail="station not found")
        else:
            station_id = target_entity_id
        return station_id
