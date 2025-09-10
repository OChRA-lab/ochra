import logging
from pathlib import Path
from ochra_common.utils.logging_config import (
    get_standard_format,
    get_detailed_format,
    get_console_handler,
    get_rotating_file_handler,
    get_logger_config,
)


def configure_station_logging(log_root_path: Path, console_log_level: int = logging.INFO):
    """
    Configures logging for the lab management system.

    Args:
        log_root_path (Path): The root directory where log files will be stored.
        log_level (int): The logging level (e.g., logging.INFO, logging.DEBUG).
    """
    logging_dir = log_root_path.joinpath("logs")
    logging_dir.mkdir(parents=True, exist_ok=True)

    # Dictionary to configure logging
    logging_config_dict = {
        "version": 1,
        "disable_existing_loggers": False,
        # Formatters
        "formatters": {
            "standard": {"format": get_standard_format()},
            "detailed": {"format": get_detailed_format()},
        },
        # Handlers
        "handlers": {
            "console_handler": get_console_handler(
                formatter="standard", level=console_log_level
            ),
            "station_server_handler": get_rotating_file_handler(
                formatter="detailed", file_path=str(logging_dir / "station_server.log")
            ),
            "lab_connection_handler": get_rotating_file_handler(
                formatter="detailed", file_path=str(logging_dir / "lab_connection.log")
            ),
        },
        # Loggers
        "root": {
            "level": "NOTSET",
            "handlers": ["console_handler"],
            "propagate": False,
        },
        "loggers": {
            # Station server loggers
            "ochra_manager.station.station_server": get_logger_config(
                handlers=["console_handler", "station_server_handler"],
                level=logging.DEBUG,
                propagate=False,
            ),
            "ochra_common.connections.lab_connection": get_logger_config(
                handlers=["console_handler", "lab_connection_handler"],
                level=logging.DEBUG,
                propagate=False,
            ),
        },
    }

    logging.config.dictConfig(logging_config_dict)

def configure_device_logger(log_root_path: Path, device_module_path: str, device_name: str, console_log_level: int = logging.INFO):
    """
    Configures a logger for a specific device.

    Args:
        log_root_path (Path): The root directory where log files will be stored.
        device_name (str): The name of the device for which the logger is being configured.
        console_log_level (int): The logging level for console output (e.g., logging.INFO, logging.DEBUG).
    """
    logging_dir = log_root_path.joinpath("logs/devices")
    logging_dir.mkdir(parents=True, exist_ok=True)

    logger_name = device_module_path
    logger = logging.getLogger(logger_name)
    logger.setLevel(logging.DEBUG)

    # Create handlers
    console_handler = logging.StreamHandler()
    console_handler.setLevel(console_log_level)
    console_formatter = logging.Formatter(get_standard_format())
    console_handler.setFormatter(console_formatter)

    file_handler = logging.handlers.TimedRotatingFileHandler(
        filename=str(logging_dir / f"{device_name}.log"),
        when="midnight",
        backupCount=7,
    )
    file_handler.setLevel(logging.DEBUG)
    file_formatter = logging.Formatter(get_detailed_format())
    file_handler.setFormatter(file_formatter)

    # Add handlers to the logger
    logger.addHandler(console_handler)
    logger.addHandler(file_handler)

