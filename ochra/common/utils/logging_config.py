import logging
from typing import Dict, Tuple, List


def get_standard_format():
    """
    Get the standard log message format.
    """
    return "[%(levelname)s - %(asctime)s][%(name)s]: %(message)s"


def get_detailed_format():
    """
    Get the detailed log message format.
    """
    return "[%(levelname)s - %(asctime)s - Line(%(lineno)d)][%(name)s]: %(message)s"


def get_console_handler(formatter: str, level: int = logging.INFO) -> Dict:
    """
    Get the console handler configuration.

    Args:
        formatter (str): The formatter to use.
        level (int, optional): The logging level. Defaults to logging.INFO.

    Returns:
        dict: The console handler configuration.
    """
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
    toaddrs: List[str],
    subject: str,
    credentials: Tuple[str, str] | None = None,
    secure: Tuple = (),
    level: int = logging.DEBUG,
) -> Dict:
    """
    Get the SMTP handler configuration.

    Args:
        formatter (str): The formatter to use.
        mailhost (str): The mail server host.
        fromaddr (str): The sender's email address.
        toaddrs (List[str]): The recipient email addresses.
        subject (str): The email subject.
        credentials (Tuple[str, str] | None, optional): The SMTP server credentials. Defaults to None.
        secure (Tuple, optional): The secure connection parameters. Defaults to ().
        level (int, optional): The logging level. Defaults to logging.DEBUG.

    Returns:
        dict: The SMTP handler configuration.
    """
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
) -> Dict:
    """
    Get the rotating file handler configuration.

    Args:
        formatter (str): The formatter to use.
        file_path (str): The path to the log file.
        level (int, optional): The logging level. Defaults to logging.DEBUG.

    Returns:
        dict: The rotating file handler configuration.
    """
    return {
        "class": "logging.handlers.TimedRotatingFileHandler",
        "level": logging.getLevelName(level),
        "formatter": formatter,
        "filename": file_path,
        "when": "midnight",
        "backupCount": 7,
    }


def get_logger_config(
    handlers: List[str],
    level: int = logging.INFO,
    propagate: bool = False,
) -> Dict:
    """
    Get the logger configuration.

    Args:
        handlers (List[str]): The list of handlers to use.
        level (int, optional): The logging level. Defaults to logging.INFO.
        propagate (bool, optional): Whether to propagate the log messages. Defaults to False. 
    """
    return {
        "handlers": handlers,
        "level": logging.getLevelName(level),
        "propagate": propagate,
    }
