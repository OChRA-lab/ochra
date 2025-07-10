import inspect
import logging
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
LOG_DIR = WORKSPACE_ROOT / "ochra_logs"

_default_getLogger = logging.getLogger()
_device_logger_cache = {}

def _get_device_module():
    frame = inspect.currentframe()
    try:
        caller_frame = frame.f_back
        while caller_frame:
            module_name = caller_frame.f_globals.get("__name__")
            if module_name and "handler" in module_name:
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

    # Use the default logger if not an OChRA device
    if name != "ochra_device":
        return _default_getLogger(name)
    
    logger_name = _get_device_module()
    if logger_name in _device_logger_cache:
        return _device_logger_cache[logger_name]
    
    # Extract device name from module for the log file
    parts = logger_name.split(".")
    if len(parts) >= 2:
        device_name = parts[0]
    else:
        device_name = logger_name

