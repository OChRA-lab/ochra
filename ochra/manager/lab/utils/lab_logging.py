import logging
from pathlib import Path
from ochra.common.utils.logging_config import (
    get_standard_format,
    get_detailed_format,
    get_console_handler,
    get_rotating_file_handler,
    get_logger_config,
)


def configure_lab_logging(log_root_path: str, console_log_level: int = logging.INFO) -> None:
    """
    Configures logging for the lab management system.

    Args:
        log_root_path (str): The root directory where log files will be stored.
        console_log_level (int): The logging level for the console output (e.g., logging.INFO, logging.DEBUG).
    """
    logging_dir = Path(log_root_path).joinpath("logs")
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
            "lab_server_handler": get_rotating_file_handler(
                formatter="detailed", file_path=str(logging_dir / "lab_server.log")
            ),
            "scheduler_handler": get_rotating_file_handler(
                formatter="detailed", file_path=str(logging_dir / "scheduler.log")
            ),
            "routers_handler": get_rotating_file_handler(
                formatter="detailed", file_path=str(logging_dir / "routers.log")
            ),
            "db_connection_handler": get_rotating_file_handler(
                formatter="detailed", file_path=str(logging_dir / "db_connection.log")
            ),
            "station_connection_handler": get_rotating_file_handler(
                formatter="detailed",
                file_path=str(logging_dir / "station_connection.log"),
            ),
        },
        # Loggers
        "root": {
            "level": "NOTSET",
            "handlers": ["console_handler"],
            "propagate": False,
        },
        "loggers": {
            "ochra.manager.lab.lab_server": get_logger_config(
                handlers=["console_handler", "lab_server_handler"],
                level=logging.DEBUG,
                propagate=False,
            ),
            "ochra.manager.lab.lab_service": get_logger_config(
                handlers=["console_handler", "lab_server_handler"],
                level=logging.DEBUG,
                propagate=False,
            ),
            "ochra.manager.lab.scheduler": get_logger_config(
                handlers=["console_handler", "scheduler_handler"],
                level=logging.DEBUG,
                propagate=False,
            ),
            "ochra.manager.lab.routers.device_router": get_logger_config(
                handlers=["console_handler", "routers_handler"],
                level=logging.DEBUG,
                propagate=False,
            ),
            "ochra.manager.lab.routers.lab_router": get_logger_config(
                handlers=["console_handler", "routers_handler"],
                level=logging.DEBUG,
                propagate=False,
            ),
            "ochra.manager.lab.routers.operation_results_router": get_logger_config(
                handlers=["console_handler", "routers_handler"],
                level=logging.DEBUG,
                propagate=False,
            ),
            "ochra.manager.lab.routers.operation_router": get_logger_config(
                handlers=["console_handler", "routers_handler"],
                level=logging.DEBUG,
                propagate=False,
            ),
            "ochra.manager.lab.routers.robot_router": get_logger_config(
                handlers=["console_handler", "routers_handler"],
                level=logging.DEBUG,
                propagate=False,
            ),
            "ochra.manager.lab.routers.station_router": get_logger_config(
                handlers=["console_handler", "routers_handler"],
                level=logging.DEBUG,
                propagate=False,
            ),
            "ochra.manager.lab.routers.storage_router": get_logger_config(
                handlers=["console_handler", "routers_handler"],
                level=logging.DEBUG,
                propagate=False,
            ),
            "ochra.manager.lab.routers.ui_router": get_logger_config(
                handlers=["console_handler", "routers_handler"],
                level=logging.DEBUG,
                propagate=False,
            ),
            "ochra.manager.connections.db_connection": get_logger_config(
                handlers=["console_handler", "db_connection_handler"],
                level=logging.DEBUG,
                propagate=False,
            ),
            "ochra.manager.connections.station_connection": get_logger_config(
                handlers=["console_handler", "station_connection_handler"],
                level=logging.DEBUG,
                propagate=False,
            ),
        },
    }
    
    logging.config.dictConfig(logging_config_dict)
