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
        self.rest_adapter: RestAdapter = RestAdapter(hostname, api_key, ssl_verify, logger)

    def construct_object(self, object_type, catalogue_module, **kwargs) -> Result:
        """create data structure for object construct api and
            call on endpoint object/construct

        Args:
            object_type (_type_): type of object to construct

        Returns:
            Result: api response (should be id of object)
        """
        data = {
            "object_type": object_type.__name__,
            "catalogue_module": catalogue_module,
        }
        data["contstructor_params"] = kwargs
        result = self.rest_adapter.post(endpoint="object/construct", data=data)
        return result.data

    def call_on_object(self, object_id, object_function, **kwargs) -> Result:
        """call object function on object_id through api endpoint object/call/

        Args:
            object_id (_type_): id of object to call on
            object_function (_type_): function to call on object

        Returns:
            Result: api response
        """
        data = {"object_function": object_function}
        data["args"] = kwargs
        result = self.rest_adapter.post(
            endpoint=f"object/call/{object_id}", data=data)
        return result

    def get_object(self, object_id) -> Result:
        """get request endpoint object/get using object id

        Args:
            object_id (_type_): id of object to get

        Returns:
            Result: api response
        """
        result = self.rest_adapter.get(endpoint=f"object/get/{object_id}")
        return result.data

    def patch_object(self, object_id, **kwargs) -> Result:
        """patch request at endpoint object/set using object id and args

        Args:
            object_id (_type_): id of object to patch

        Returns:
            Result: api response
        """
        data = {}
        data["properties"] = kwargs
        result = self.rest_adapter.patch(
            endpoint=f"object/set/{object_id}", data=data)
        return result

    def create_station(self) -> Result:
        """create station using api endpoint station/create

        Returns:
            Result: api response
        """
        result = self.rest_adapter.post(endpoint="station/create")
        return result.data
