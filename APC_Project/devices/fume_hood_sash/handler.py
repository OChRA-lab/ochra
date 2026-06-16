from __future__ import annotations

import logging

from ochra.common.utils.enum import ActivityStatus
from ochra.common.utils.mixins import RestProxyMixin
from ochra.common.equipment.device import HTMLForm, CircularRangeInput


from .abstract import FumeHoodSash
from .driver import FumeHoodSashDriver


logger = logging.getLogger(__name__)


class FumeHoodSash(FumeHoodSash, RestProxyMixin):
    """Station-side OChRA wrapper for the Opta-backed fume hood sash."""

    def __init__(
        self,
        name: str,
        *,
        connection_mode: str = "tcp",
        address: str = FumeHoodSashDriver.DEFAULT_ADDRESS,
        port: int = FumeHoodSashDriver.DEFAULT_PORT,
        simulation: bool = False,
        movement_delay_seconds: float = FumeHoodSashDriver.DEFAULT_MOVEMENT_DELAY_SECONDS,
        connect_on_init: bool = True,
    ) -> None:
        super().__init__(
            name=name,
            module_path="ochra_apc_devices.devices.fume_hood_sash.device",
            collection="devices",
            connection_mode=connection_mode,
            address=address,
            port=port,
            simulation_enabled=simulation,
        )
        self._mixin_hook(self._endpoint, self.id)
        self._driver = FumeHoodSashDriver(
            device_name=name,
            connection_mode=connection_mode,
            address=address,
            port=port,
            simulation=simulation,
            movement_delay_seconds=movement_delay_seconds,
        )
        if connect_on_init:
            self.connect_device()

    def _record_error(self, exc: Exception) -> None:
        self.last_error = str(exc)
        self.status = ActivityStatus.ERROR
        logger.error("Fume hood sash error on %s: %s", self.name, exc)

    def _refresh_snapshot(self) -> None:
        status = self._driver.status()
        self.connected = bool(status["connected"])
        self.piston_up = bool(status["piston_up"])
        self.sash_up = bool(status["sash_up"])
        self.last_command = status["last_command"]
        self.last_reply = status["last_reply"]
        self.last_error = str(status["last_error"] or "")

    def _require_connection(self) -> None:
        if not self.connected:
            self.connect_device()

    def connect_device(self) -> bool:
        try:
            self._driver.connect()
            self.status = ActivityStatus.IDLE
            self.last_error = ""
            self._refresh_snapshot()
            return True
        except Exception as exc:
            self.connected = False
            self._record_error(exc)
            raise

    def disconnect_device(self) -> bool:
        self._driver.disconnect()
        self.connected = False
        self.status = ActivityStatus.IDLE
        self.last_error = ""
        return True

    def is_connected(self) -> bool:
        return self._driver.is_connected()

    def is_idle(self) -> bool:
        return self._driver.is_idle()
    
    @HTMLForm(call="move_up", method="POST")
    def move_up(self) -> dict[str, object]:
        self._require_connection()
        result = self._driver.move_up()
        self._refresh_snapshot()
        return result

    @HTMLForm(call="move_down", method="POST")
    def move_down(self) -> dict[str, object]:
        self._require_connection()
        result = self._driver.move_down()
        self._refresh_snapshot()
        return result

    def verification_details(self) -> dict[str, object]:
        return self._driver.verification_details()

    def verify_binding(self) -> dict[str, object]:
        return self._driver.verify_binding()

    def status_snapshot(self) -> dict[str, object]:
        self._refresh_snapshot()
        return self._driver.status()
