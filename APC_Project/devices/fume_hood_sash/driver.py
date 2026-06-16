# Opta mapping: Opta 3, relay 1

from __future__ import annotations

import socket
import time
from typing import Any


class FumeHoodSashDriver:
    """TCP driver for the Opta-backed fume hood sash."""

    DEFAULT_ADDRESS = "192.168.1.53"
    DEFAULT_PORT = 5000
    DEFAULT_TIMEOUT_SECONDS = 5.0
    DEFAULT_MOVEMENT_DELAY_SECONDS = 10.0

    MOVE_UP_COMMAND = "R1_ON"
    MOVE_DOWN_COMMAND = "R1_OFF"
    STATUS_COMMAND = "STATUS"




    def __init__(
        self,
        *,
        device_name: str,
        connection_mode: str,
        address: str | None,
        port: int | str,
        simulation: bool,
        timeout_seconds: float = DEFAULT_TIMEOUT_SECONDS,
        movement_delay_seconds: float = DEFAULT_MOVEMENT_DELAY_SECONDS,
    ) -> None:
        del device_name
        if connection_mode not in {"tcp", "ethernet"}:
            raise ValueError("Fume hood sash supports only tcp connection mode.")

        self._address = str(address or self.DEFAULT_ADDRESS)
        self._port = int(port)
        self._simulation = simulation
        self._timeout_seconds = float(timeout_seconds)
        self._movement_delay_seconds = float(movement_delay_seconds)

        self._connected = False
        self._last_command: str | None = None
        self._last_reply: str | None = None
        self._last_error: str | None = None
        self._piston_up = False
        self._sash_up = False

    @property
    def simulation(self) -> bool:
        return self._simulation

    @property
    def address(self) -> str:
        return self._address

    @property
    def port(self) -> int:
        return self._port

    def connect(self) -> None:
        if self._connected:
            return
        if self._simulation:
            self._connected = True
            return
        self._send_command(self.STATUS_COMMAND)
        self._connected = True

    def disconnect(self) -> None:
        self._connected = False

    def is_connected(self) -> bool:
        if self._simulation:
            return self._connected
        try:
            self._send_command(self.STATUS_COMMAND)
            self._connected = True
            return True
        except Exception:
            self._connected = False
            return False

    def is_idle(self) -> bool:
        return self.is_connected()

    def move_up(self) -> dict[str, Any]:
        return self._set_state(True, self.MOVE_UP_COMMAND)

    def move_down(self) -> dict[str, Any]:
        return self._set_state(False, self.MOVE_DOWN_COMMAND)

    def verification_details(self) -> dict[str, Any]:
        if self._simulation:
            return {
                "supported": True,
                "strategy": "simulation",
                "command": self.STATUS_COMMAND,
                "human_message": "Simulation mode: verification is virtual.",
            }
        return {
            "supported": True,
            "strategy": "read_command",
            "command": self.STATUS_COMMAND,
            "human_message": "Checks that the Opta responds to the STATUS command.",
        }

    def verify_binding(self) -> dict[str, Any]:
        details = self.verification_details()
        if self._simulation:
            return {
                **details,
                "verified": True,
                "manual_check_required": False,
                "message": "Simulation verification succeeded.",
            }
        try:
            self.connect()
            return {
                **details,
                "verified": True,
                "manual_check_required": False,
                "message": "Verification succeeded.",
            }
        except Exception as exc:
            return {
                **details,
                "verified": False,
                "manual_check_required": False,
                "message": f"Verification failed: {exc}",
            }

    def status(self) -> dict[str, Any]:
        return {
            "connected": self._connected,
            "simulation": self._simulation,
            "hardware_backend_active": (not self._simulation) and self._connected,
            "address": self._address,
            "port": self._port,
            "last_command": self._last_command,
            "last_reply": self._last_reply,
            "last_error": self._last_error,
            "piston_up": self._piston_up,
            "sash_up": self._sash_up,
        }

    def _set_state(self, piston_up: bool, command: str) -> dict[str, Any]:
        if not self._simulation:
            self.connect()
        reply = "SIM" if self._simulation else self._send_command(command)
        self._last_command = command
        self._last_reply = reply
        self._last_error = None
        self._piston_up = piston_up
        self._sash_up = piston_up
        result = {
            "ok": True,
            "simulated": self._simulation,
            "address": self._address,
            "port": self._port,
            "command": command,
            "reply": reply,
            "piston_up": piston_up,
            "sash_up": self._sash_up,
            "state": "UP" if piston_up else "DOWN",
        }
        self._apply_movement_delay()
        return result

    def _send_command(self, command: str) -> str:
        try:
            with socket.create_connection(
                (self._address, self._port), timeout=self._timeout_seconds
            ) as sock:
                sock.settimeout(self._timeout_seconds)
                sock.sendall(f"{command}\n".encode("utf-8"))
                chunks: list[bytes] = []
                while True:
                    try:
                        data = sock.recv(4096)
                    except socket.timeout:
                        break
                    if not data:
                        break
                    chunks.append(data)
        except OSError as exc:
            self._last_error = str(exc)
            raise RuntimeError(f"Opta command failed: {exc}") from exc
        return b"".join(chunks).decode("utf-8", errors="replace").strip()

    def _apply_movement_delay(self) -> None:
        if self._movement_delay_seconds > 0:
            time.sleep(self._movement_delay_seconds)
