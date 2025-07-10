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

_default_getLogger = logging.getLogger

def custom_getLogger(name=None):

    # Use the default logger if not an OChRA device
    if name != "ochra_device":
        return _default_getLogger(name)