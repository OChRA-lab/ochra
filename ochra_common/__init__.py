from .utils.logging_config import configure_logging


def _configure_ochra():
    """Initialise the OChRA framework."""
    configure_logging()


_configure_ochra()
