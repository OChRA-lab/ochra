import logging
import logging.config
import logging.handlers
import inspect
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
        "info_handler": {
            "class": "logging.handlers.TimedRotatingFileHandler",
            "level": "INFO",
            "filters": ["info_pass_filter"],
            "formatter": "standard",
            "filename": str(LOG_DIR / "ochra_info.log"),
            "when": "midnight",
            "backupCount": 7,
        },
        "error_handler": {
            "class": "logging.handlers.TimedRotatingFileHandler",
            "level": "WARNING",
            "formatter": "detailed",
            "filename": str(LOG_DIR / "ochra_error.log"),
            "when": "midnight",
            "backupCount": 7,
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
        "handlers": ["console_handler", "info_handler", "error_handler"],
        "propagate": False,
    },
    "loggers": {

        # Lab server loggers
        "lab_server": {
            "level": "DEBUG",
            "handlers": ["lab_server_handler"],
            "propagate": True,
        },
        "scheduler": {
            "level": "DEBUG",
            "handlers": ["scheduler_handler"],
            "propagate": True,
        },
        "device_router": {
            "level": "DEBUG",
            "handlers": ["routers_handler"],
            "propagate": True,
        },
        "lab_router": {
            "level": "DEBUG",
            "handlers": ["routers_handler"],
            "propagate": True,
        },
        "operation_results_router": {
            "level": "DEBUG",
            "handlers": ["routers_handler"],
            "propagate": True,
        },
        "operation_router": {
            "level": "DEBUG",
            "handlers": ["routers_handler"],
            "propagate": True,
        },
        "robot_router": {
            "level": "DEBUG",
            "handlers": ["routers_handler"],
            "propagate": True,
        },
        "station_router": {
            "level": "DEBUG",
            "handlers": ["routers_handler"],
            "propagate": True,
        },
        "storage_router": {
            "level": "DEBUG",
            "handlers": ["routers_handler"],
            "propagate": True,
        },
        "ui_router": {
            "level": "DEBUG",
            "handlers": ["routers_handler"],
            "propagate": True,
        },
        "db_connection": {
            "level": "DEBUG",
            "handlers": ["db_connection_handler"],
            "propagate": True,
        },
        "station_connection": {
            "level": "DEBUG",
            "handlers": ["station_connection_handler"],
            "propagate": True,
        },

        # Station server loggers
        "station_server": {
            "level": "DEBUG",
            "handlers": ["station_server_handler"],
            "propagate": True,
        },
        "lab_connection": {
            "level": "DEBUG",
            "handlers": ["lab_connection_handler"],
            "propagate": True,
        },
        "ochra_device": {
            "level": "DEBUG",
            "handlers": [],
            "propagate": True,
        },
        
        # Client devices loggers
        "experiment": {
            "level": "DEBUG",
            "handlers": ["experiment_handler"],
            "propagate": True,
        },
    },
}


_default_getLogger = logging.getLogger
_device_logger_cache = {}


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


def _create_device_handler(device_name):
    """Dynamically create a handler for a specific device."""
    # Sanitise device name and create log file path
    safe_device_name = "".join(
        c for c in device_name if c.isalnum() or c in ("_", "-")
    ).rstrip()
    devices_log_dir = LOG_DIR / "devices"
    devices_log_dir.mkdir(parents=True, exist_ok=True)
    log_file = devices_log_dir / f"{safe_device_name}.log"

    # Create and configure the handler
    handler = logging.handlers.TimedRotatingFileHandler(
        filename=str(log_file), when="midnight", backupCount=7
    )
    handler.setLevel(logging.DEBUG)
    formatter = logging.Formatter(
        "%(asctime)s - %(levelname)s - %(name)s - %(message)s"
    )
    handler.setFormatter(formatter)

    return handler


def custom_getLogger(name=None):
    """ Replace the default getLogger to handle OChRA devices."""
    # Use the default logger if not an OChRA device
    if name != "ochra_device":
        return _default_getLogger(name)

    # Check if the logger is already cached
    logger_name = _get_device_module()
    if logger_name and logger_name in _device_logger_cache:
        return _device_logger_cache[logger_name]

    # Use the default logger if no device module found,
    if logger_name is None:
        return _default_getLogger("name")

    # Extract device name from module for the log file
    parts = logger_name.split(".")
    if len(parts) >= 2:
        device_name = parts[0]
    else:
        device_name = logger_name

    # Get device logger and add a handler
    device_logger = _default_getLogger(logger_name)
    if not device_logger.handlers:
        handler = _create_device_handler(device_name)
        device_logger.addHandler(handler)
        device_logger.setLevel(logging.DEBUG)
        device_logger.propagate = False

    # Cache the logger
    _device_logger_cache[logger_name] = device_logger

    return device_logger


def configure_logging():
    """Configure the custom logging system."""
    LOG_DIR.mkdir(parents=True, exist_ok=True)
    logging.config.dictConfig(LOGGING_CONFIG_DICT)
    logging.getLogger = custom_getLogger


configure_logging()
