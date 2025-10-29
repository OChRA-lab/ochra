from ochra_manager.connections.db_connection import DbConnection
from ochra_common.equipment.operation import Operation
from threading import Thread
from time import sleep
from ochra_common.utils.enum import ActivityStatus, PatchType
from fastapi import HTTPException
from ...connections.station_connection import StationConnection
import logging


class Scheduler:
    """
    A class to manage and schedule operations in the lab.

    Attributes:
        op_queue (list): A list to hold the queued operations.
    """
    def __init__(self):
        self._logger = logging.getLogger(__name__)
        self.op_queue = []
        self._db_conn: DbConnection = DbConnection()
        self._stop = False
        
        # create operation queue in db
        self._queue_id = self._db_conn.create(
            {"_collection": "lab"}, {"op_queue": self.op_queue}
        )

    def add_operation(self, operation: Operation) -> None:
        """
            Adds an operation to the scheduling queue.

            Args:
                operation (Operation): The operation to be added to the queue.
        """
        self._logger.debug(f"Adding operation {operation.id} to queue")
        self.op_queue.append(operation)

    def run(self) -> None:
        """
        Starts the scheduling thread.
        """
        self.thread = Thread(target=self._schedule, daemon=False)
        self.thread.start()

    def _schedule(self) -> None:
        """
        The main scheduling loop that processes operations in the queue.
        """
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
                        self._logger.debug(f"Starting operation execution for {operation.id}")
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

    def stop(self) -> None:
        """
        Stops the scheduling thread.
        """
        self._stop = True
        self.thread.join()

    def _execute_op(self, operation: Operation, station_id: str) -> None:
        """
        Executes the given operation on the specified station.

        Args:
            operation (Operation): The operation to be executed.
            station_id (str): The ID of the station where the operation will be executed.
        """
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

    def _resolve_station_id(self, op: Operation) -> str:
        """
        Resolves the station ID for the given operation.

        Args:
            op (Operation): The operation for which to resolve the station ID.
        
        Returns:
            str: The resolved station ID.
        """
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
