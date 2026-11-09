"""Disabled standalone solid addition station.

Solid addition shares the Arduino Uno on COM4 with the base valve, so it must
run in the same Python process as the base valve station. Use
base_valve_station.py, which registers both devices on one StationServer.
"""


if __name__ == "__main__":
    print(
        "solid_addition_station.py is disabled. "
        "Start base_valve_station.py for the consolidated COM4 station."
    )
