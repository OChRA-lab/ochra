import logging


def get_standard_format():
    return "[%(levelname)s - %(asctime)s][%(name)s]: %(message)s"


def get_detailed_format():
    return "[%(levelname)s - %(asctime)s - Line(%(lineno)d)][%(name)s]: %(message)s"


def get_console_handler(formatter: str, level: int = logging.INFO):
    return {
        "class": "logging.StreamHandler",
        "level": logging.getLevelName(level),
        "formatter": formatter,
        "stream": "ext://sys.stdout",
    }


def get_smtp_handler(
    formatter: str,
    mailhost: str,
    fromaddr: str,
    toaddrs: list[str],
    subject: str,
    credentials: tuple[str, str] | None = None,
    secure: tuple = (),
    level: int = logging.DEBUG,
):
    return {
        "class": "logging.handlers.SMTPHandler",
        "level": logging.getLevelName(level),
        "formatter": formatter,
        "mailhost": mailhost,
        "fromaddr": fromaddr,
        "toaddrs": toaddrs,
        "subject": subject,
        "credentials": credentials,
        "secure": secure,
    }


def get_rotating_file_handler(
    formatter: str, file_path: str, level: int = logging.DEBUG
):
    return {
        "class": "logging.handlers.TimedRotatingFileHandler",
        "level": logging.getLevelName(level),
        "formatter": formatter,
        "filename": file_path,
        "when": "midnight",
        "backupCount": 7,
    }


def get_logger_config(
    handlers: list[str],
    level: int = logging.INFO,
    propagate: bool = False,
):
    return {
        "handlers": handlers,
        "level": logging.getLevelName(level),
        "propagate": propagate,
    }
