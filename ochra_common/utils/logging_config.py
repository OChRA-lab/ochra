import inspect
import logging
import logging.config
from pathlib import Path


# Filter to allow INFO level only
class InfoPassFilter(logging.Filter):
    def filter(self, record):
        return record.levelno == logging.INFO


# Find OChRA root and set log directory
current_path = Path(__file__).resolve()
for parent in current_path.parents:
    if ((parent / "ochra_common").exists() and (parent / "ochra_manager").exists()) or (
        (parent / "ochra_common").exists() and (parent / "ochra_discovery").exists()
    ):
        WORKSPACE_ROOT = parent
        break
LOG_DIR = WORKSPACE_ROOT / "ochra_logs"

# Dictionary to configure logging
LOGGING_CONFIG_DICT = {
    "version": 1,
    "disable_existing_loggers": False,
    # Formatters
    "formatters": {
        "simple": {  # log level - message
            "format": "%(levelname)s - %(message)s"
        },
        "standard": {  # ISO-8601 timestamp - log level - logger name - message
            "format": "%(asctime)s - %(levelname)s - %(name)s - %(message)s"
        },
        "detailed": {  # timestamp - log level - logger name - function: line number - message
            "format": "%(asctime)s - %(levelname)s - %(name)s - Line: %(lineno)d - %(message)s"
        },
    },
    # Filters
    "filters": {
        "info_pass_filter": {
            "()": InfoPassFilter,
        },
    },
    # Handlers
    "handlers": {
        "console_handler": {
            "class": "logging.StreamHandler",
            "level": "INFO",
            "formatter": "simple",
            "stream": "ext://sys.stdout",
        },
        "console_error_handler": {
            "class": "logging.StreamHandler",
            "level": "WARNING",
            "formatter": "detailed",
            "stream": "ext://sys.stdout",
        },
        # "critical_handler": {
        #    "level": "CRITICAL",
        #    "formatter": "detailed",
        #    "class": "logging.handlers.SMTPHandler",
        #    "mailhost" : "mailserver",
        #    "fromaddr": "sender@example.com",
        #    "toaddrs": ["recipient@example.com"],
        #    "subject": "Critical error in OChRA framework"
        # },
        # Lab server handlers
        "lab_server_handler": {
            "class": "logging.handlers.TimedRotatingFileHandler",
            "level": "DEBUG",
            "formatter": "standard",
            "filename": str(LOG_DIR / "lab_server.log"),
            "when": "midnight",
            "backupCount": 7,
        },
        "lab_service_handler": {
            "class": "logging.handlers.TimedRotatingFileHandler",
            "level": "DEBUG",
            "formatter": "standard",
            "filename": str(LOG_DIR / "lab_service.log"),
            "when": "midnight",
            "backupCount": 7,
        },
        "scheduler_handler": {
            "class": "logging.handlers.TimedRotatingFileHandler",
            "level": "DEBUG",
            "formatter": "standard",
            "filename": str(LOG_DIR / "scheduler.log"),
            "when": "midnight",
            "backupCount": 7,
        },
        "routers_handler": {
            "class": "logging.handlers.TimedRotatingFileHandler",
            "level": "DEBUG",
            "formatter": "standard",
            "filename": str(LOG_DIR / "routers.log"),
            "when": "midnight",
            "backupCount": 7,
        },
        "db_connection_handler": {
            "class": "logging.handlers.TimedRotatingFileHandler",
            "level": "DEBUG",
            "formatter": "standard",
            "filename": str(LOG_DIR / "db_connection.log"),
            "when": "midnight",
            "backupCount": 7,
        },
        "station_connection_handler": {
            "class": "logging.handlers.TimedRotatingFileHandler",
            "level": "DEBUG",
            "formatter": "standard",
            "filename": str(LOG_DIR / "station_connection.log"),
            "when": "midnight",
            "backupCount": 7,
        },
        # Station server handlers
        "station_server_handler": {
            "class": "logging.handlers.TimedRotatingFileHandler",
            "level": "DEBUG",
            "formatter": "standard",
            "filename": str(LOG_DIR / "station_server.log"),
            "when": "midnight",
            "backupCount": 7,
        },
        "lab_connection_handler": {
            "class": "logging.handlers.TimedRotatingFileHandler",
            "level": "DEBUG",
            "formatter": "standard",
            "filename": str(LOG_DIR / "lab_connection.log"),
            "when": "midnight",
            "backupCount": 7,
        },
        # Client handlers
        "experiment_handler": {
            "class": "logging.handlers.TimedRotatingFileHandler",
            "level": "DEBUG",
            "formatter": "standard",
            "filename": str(LOG_DIR / "experiment.log"),
            "when": "midnight",
            "backupCount": 7,
        },
    },
    # Loggers
    "root": {
        "level": "NOTSET",
        "handlers": ["console_error_handler"],
        "propagate": False,
    },
    "loggers": {
        # Lab server loggers
        "ochra_manager.lab.lab_server": {
            "level": "DEBUG",
            "handlers": ["console_handler", "lab_server_handler"],
            "propagate": True,
        },
        "ochra_manager.lab.lab_service": {
            "level": "DEBUG",
            "handlers": ["console_handler", "lab_service_handler"],
            "propagate": True,
        },
        "ochra_manager.lab.scheduler": {
            "level": "DEBUG",
            "handlers": ["console_handler", "scheduler_handler"],
            "propagate": True,
        },
        "ochra_manager.lab.routers.device_router": {
            "level": "DEBUG",
            "handlers": ["console_handler", "routers_handler"],
            "propagate": True,
        },
        "ochra_manager.lab.routers.lab_router": {
            "level": "DEBUG",
            "handlers": ["console_handler", "routers_handler"],
            "propagate": True,
        },
        "ochra_manager.lab.routers.operation_results_router": {
            "level": "DEBUG",
            "handlers": ["console_handler", "routers_handler"],
            "propagate": True,
        },
        "ochra_manager.lab.routers.operation_router": {
            "level": "DEBUG",
            "handlers": ["console_handler", "routers_handler"],
            "propagate": True,
        },
        "ochra_manager.lab.routers.robot_router": {
            "level": "DEBUG",
            "handlers": ["console_handler", "routers_handler"],
            "propagate": True,
        },
        "ochra_manager.lab.routers.station_router": {
            "level": "DEBUG",
            "handlers": ["console_handler", "routers_handler"],
            "propagate": True,
        },
        "ochra_manager.lab.routers.storage_router": {
            "level": "DEBUG",
            "handlers": ["console_handler", "routers_handler"],
            "propagate": True,
        },
        "ochra_manager.lab.routers.ui_router": {
            "level": "DEBUG",
            "handlers": ["console_handler", "routers_handler"],
            "propagate": True,
        },
        "ochra_manager.connections.db_connection": {
            "level": "DEBUG",
            "handlers": ["console_handler", "db_connection_handler"],
            "propagate": True,
        },
        "ochra_manager.connections.station_connection": {
            "level": "DEBUG",
            "handlers": ["console_handler", "station_connection_handler"],
            "propagate": True,
        },
        # Station server loggers
        "ochra_manager.station.station_server": {
            "level": "DEBUG",
            "handlers": ["console_handler", "station_server_handler"],
            "propagate": True,
        },
        "ochra_common.connections.lab_connection": {
            "level": "DEBUG",
            "handlers": ["console_handler", "lab_connection_handler"],
            "propagate": True,
        },
        "ochra_device": {
            "level": "DEBUG",
            "handlers": ["console_handler"],
            "propagate": True,
        },
        # Client devices loggers
        "experiment": {
            "level": "DEBUG",
            "handlers": ["console_handler", "experiment_handler"],
            "propagate": True,
        },
    },
}


# Store the original getLogger function
_default_getLogger = logging.getLogger


def _get_device_module():
    """Find the device module name from the call stack"""
    frame = inspect.currentframe()
    try:
        # Traverse up the call stack to find the device module
        caller_frame = frame.f_back
        while caller_frame:
            # Only accept modules that end with ".handler"
            module_name = caller_frame.f_globals.get("__name__")
            if module_name and module_name.endswith(".handler"):
                return module_name
            caller_frame = caller_frame.f_back
    finally:
        del frame
    return None


def custom_getLogger(name=None):
    """Replace the default getLogger to handle OChRA devices."""
    # Use the default logger if not an OChRA device
    if name != "ochra_device":
        return _default_getLogger(name)

    # Get the device module name from the call stack
    logger_name = _get_device_module()

    # Use the default logger if no device module found
    if logger_name is None:
        return _default_getLogger(name)

    # Extract device name from module for the log file
    parts = logger_name.split(".")
    if len(parts) >= 2:
        device_name = parts[0]
    else:
        device_name = logger_name

    # Sanitise device name and create log file path and handler name
    safe_device_name = "".join(
        c for c in device_name if c.isalnum() or c in ("_", "-")
    ).rstrip()
    devices_log_dir = LOG_DIR / "devices"
    devices_log_dir.mkdir(parents=True, exist_ok=True)
    log_file = devices_log_dir / f"{safe_device_name}.log"
    handler_name = f"{safe_device_name}_handler"

    # Add the handler to the config dict if it doesn't exist
    if handler_name not in LOGGING_CONFIG_DICT["handlers"]:
        LOGGING_CONFIG_DICT["handlers"][handler_name] = {
            "class": "logging.handlers.TimedRotatingFileHandler",
            "level": "DEBUG",
            "formatter": "standard",
            "filename": str(log_file),
            "when": "midnight",
            "backupCount": 7,
        }

    # Add the logger to the config dict if it doesn't exist
    if logger_name not in LOGGING_CONFIG_DICT["loggers"]:
        LOGGING_CONFIG_DICT["loggers"][logger_name] = {
            "handlers": [
                "console_handler",
                handler_name,
            ],
            "level": "DEBUG",
            "propagate": True,
        }
        # Reconfigure logging with the updated configuration
        logging.config.dictConfig(LOGGING_CONFIG_DICT)

    # Return the configured logger
    return _default_getLogger(logger_name)


def configure_logging():
    """Configure the custom logging system."""
    LOG_DIR.mkdir(parents=True, exist_ok=True)
    logging.config.dictConfig(LOGGING_CONFIG_DICT)
    logging.getLogger = custom_getLogger


configure_logging()
