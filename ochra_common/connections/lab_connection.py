from ochra_common.utils.singleton_meta import SingletonMeta
from ochra_common.connections.rest_adapter import RestAdapter, Result, LabEngineException
import logging


class LabConnection(metaclass=SingletonMeta):
    """lab adapter built on top of RestAdapter,
    heavily coupled to lab engine api
    """

    def __init__(
        self,
        hostname: str = "127.0.0.1:8000",
        api_key: str = "",
        ssl_verify: bool = False,
        logger: logging.Logger = None,
    ):
        """constructor for labAdapter class

        Args:
            hostname (_type_, optional): address of lap api.
                Defaults to "127.0.0.1:8000".
            api_key (str, optional): api key if exists. Defaults to ''.
            ssl_verify (bool, optional): if we need to verify ssl.
                Defaults to False.
            logger (logging.Logger, optional): logger if you have one.
                Defaults to None.
        """
        self.rest_adapter: RestAdapter = RestAdapter(
            hostname, api_key, ssl_verify, logger)

