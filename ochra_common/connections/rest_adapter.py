import requests
import requests.packages
from typing import List, Dict
from json import JSONDecodeError
import logging
# from ochra_common import Station


class LabEngineException(Exception):
    pass


class Result:
    """Result dataclass for json to python instances
    """

    def __init__(self, status_code: int,
                 message: str = '', data: List[Dict] = None):
        """constructer for result class

        Args:
            status_code (int): HTTP statuscode
            message (str, optional): Message returned from request. Defaults to ''.
            data (List[Dict], optional): Data return from request. Defaults to None.
        """
        self.status_code = int(status_code)
        self.message = str(message)
        self.data = data if data is not None else []


class RestAdapter():
    """Rest API adapter class

    """

    def __init__(self, hostname: str, api_key: str = '',
                 ssl_verify: bool = True, logger: logging.Logger = None):
        """Constructor for RestAdapter

        Args:
            hostname (str): address of api
            api_key (str, optional): authentication string. Defaults to ''.
            ssl_verify (bool, optional): if we need to verify ssl.
                Defaults to True.
            logger (logging.Logger, optional): logger if you have one.
                Defaults to None.
        """
        self.url = f"http://{hostname}/"
        self._api_key = api_key
        self._ssl_verify = ssl_verify
        self._logger = logger or logging.getLogger(__name__)
        if not ssl_verify:
            # noinspection PyUnresolvedReferences
            requests.packages.urllib3.disable_warnings()

    def _do(self, http_method: str, endpoint: str, ep_params: Dict = None,
            data: Dict = None) -> Result:
        """ Does a request of type based on the method passed in http_method

        Args:
            http_method (str): GET POST or DELETE
            endpoint (str): endpoint in api to do the request to
            ep_params (Dict, optional): end point parameters if exist.
                Defaults to None.
            data (Dict, optional): data body (json). Defaults to None.

        Raises:
            LabEngineException: Request failure
            LabEngineException: Bad Json
            LabEngineException: Some other response

        Returns:
            Result: Data from request in the form of a Result instances
        """
        full_url = self.url + endpoint
        headers = {'x-api-key': self._api_key}
        # fix for when ep_params is empty
        log_line_pre = f"method={http_method}, " + \
            f"url={full_url}, params={
                str(ep_params).replace("{", "[").replace("}", "]")}"
        log_line_post = ', '.join(
            (log_line_pre, "success={}, status_code={}, message={}"))

        # log request and perform HTTP Request catching exceptions and re-raising
        try:
            self._logger.debug(msg=log_line_pre)
            response = requests.request(method=http_method, url=full_url,
                                        verify=self._ssl_verify,
                                        headers=headers, params=ep_params,
                                        json=data)
        except requests.exceptions.RequestException as e:
            self._logger.error(msg=str(e))
            raise LabEngineException("Request Failed") from e

        # Deserialize response into python object
        try:
            data_out = response.json()
        except (ValueError, JSONDecodeError) as e:
            self._logger.error(msg=log_line_post.format(False, None, e))
            raise LabEngineException("Bad JSON in response") from e

        # if sucess return result else raise exception
        is_success = 299 >= response.status_code >= 200
        log_line = log_line_post.format(
            is_success, response.status_code, response.reason)
        if is_success:
            self._logger.debug(msg=log_line)
            return Result(response.status_code, message=response.reason, data=data_out)
        self._logger.error(msg=log_line)
        raise LabEngineException(f"{response.status_code}: {
                                 response.reason}, {response.text}")

    def get(self, endpoint: str, ep_params: Dict = None) -> Result:
        """ do a get request to endpoint using _do

        Args:
            endpoint (str): Endpoint to request
            ep_params (Dict, optional): end point parameters if exist. Defaults to None.

        Returns:
            Result: Data from request in the form of a Result instances
        """
        return self._do(http_method='GET', endpoint=endpoint,
                        ep_params=ep_params)

    def put(self, endpoint: str, ep_params: Dict = None,
            data: Dict = None) -> Result:
        """ Do a put request to endpoint using _do

        Args:
            endpoint (str): Endpoint to request
            ep_params (Dict, optional): end point parameters if exist. Defaults to None.
            data (Dict, optional): data body (json). Defaults to None.

        Returns:
            Result: Data from request in the form of a Result instances
        """
        return self._do(http_method='PUT', endpoint=endpoint,
                        ep_params=ep_params, data=data)

    def post(self, endpoint: str, ep_params: Dict = None,
             data: Dict = None) -> Result:
        """ Do a Post request to endpoint using _do

        Args:
            endpoint (str): Endpoint to request
            ep_params (Dict, optional): end point parameters if exist. Defaults to None.
            data (Dict, optional): data body (json). Defaults to None.

        Returns:
            Result: Data from request in the form of a Result instances
        """
        return self._do(http_method='POST', endpoint=endpoint,
                        ep_params=ep_params, data=data)

    def patch(self, endpoint: str, ep_params: Dict = None,
              data: Dict = None) -> Result:
        """Do a Patch request to endpoint using _do

        Args:
            endpoint (str): Endpoint to request
            ep_params (Dict, optional): end point parameters if exist. Defaults to None.
            data (Dict, optional): data body (json). Defaults to None.

        Returns:
            Result: Data from request in the form of a Result instances
        """
        return self._do(http_method="PATCH", endpoint=endpoint,
                        ep_params=ep_params, data=data)

    def delete(self, endpoint: str, ep_params: Dict = None,
               data: Dict = None) -> Result:
        """Do a delete request to endpoint using _do

        Args:
            endpoint (str): Endpoint to request
            ep_params (Dict, optional): end point parameters if exist. Defaults to None.
            data (Dict, optional): data body (json). Defaults to None.

        Returns:
            Result: Data from request in the form of a Result instances
        """
        return self._do(http_method='DELETE', endpoint=endpoint,
                        ep_params=ep_params, data=data)


if __name__ == "__main__":
    adapter = RestAdapter("127.0.0.1:8000", ssl_verify=False)
    # doesnt do anything as adapter already exists
    adapter2 = RestAdapter("127.0.2.1:8000", ssl_verify=False)

    print(adapter2.url)
    print(adapter.url)
    data = {
        "operation": "Some Operation",
        "station": "some Station",
        # "device": "some Device",
        # "args": {
        #    "abc": 123
        # }
    }

    data2 = {
        "object_type": "Rack",
        "contstructor_params": {
            "some param": "param1",
            "some other param": "param2"
        }
    }
    print(adapter.post("Operation", data=data).message)
    print(adapter.post("ConstructObject", data=data2).data)
