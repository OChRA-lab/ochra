from .utils.logging_config import configure_logging


def _configure_framework():
    """Initialise the OChRA framework."""
    configure_logging()


_configure_framework()
