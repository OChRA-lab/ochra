import requests
import requests.packages
from typing import List, Dict
from json import JSONDecodeError
import logging
from fastapi.responses import FileResponse
# from ochra.common import Station


class LabEngineException(Exception):
    pass


class Result:
    """
    A class representing the result of an HTTP request, including status code, message, and data.
    """

    def __init__(self, status_code: int, message: str = "", data: List[Dict] = None):
        """
        Initializes a Result instance.

        Args:
            status_code (int): HTTP status code.
            message (str, optional): Message returned from the request. Defaults to "".
            data (List[Dict], optional): Data returned from the request. Defaults to None.
        """
        self.status_code = int(status_code)
        self.message = str(message)
        self.data = data if data is not None else []


class RestAdapter:
    """Adapter class for interacting with RESTful APIs."""

    def __init__(
        self,
        hostname: str,
        api_key: str = "",
        ssl_verify: bool = True,
        logger: logging.Logger = None,
    ):
        """
        Initializes the RestAdapter for interacting with a RESTful API.

        Args:
            hostname (str): The hostname or IP address of the API server.
            api_key (str, optional): API key for authentication. Defaults to ''.
            ssl_verify (bool, optional): Whether to verify SSL certificates. Defaults to True.
            logger (logging.Logger, optional): Custom logger instance. If None, a default logger is used.
        """
        self.url = f"http://{hostname}/"
        self._api_key = api_key
        self._ssl_verify = ssl_verify
        self._logger = logger or logging.getLogger(__name__)
        if not ssl_verify:
            # noinspection PyUnresolvedReferences
            requests.packages.urllib3.disable_warnings()

    def _do(
        self,
        http_method: str,
        endpoint: str,
        ep_params: Dict = None,
        data: Dict = None,
        files=None,
        jsonify=True,
    ) -> Result | requests.Response:
        """
        Executes an HTTP request using the specified method and parameters.

        Args:
            http_method (str): The HTTP method to use (e.g., 'GET', 'POST', 'PUT', 'PATCH', 'DELETE').
            endpoint (str): The API endpoint to send the request to.
            ep_params (Dict, optional): Query parameters for the endpoint. Defaults to None.
            data (Dict, optional): JSON body to include in the request. Defaults to None.
            files (Any, optional): Files to upload with the request. Defaults to None.
            jsonify (bool, optional): If True, attempts to parse the response as JSON. If False, returns the raw response.

        Raises:
            LabEngineException: If the request fails, the response contains invalid JSON, or the response status code indicates an error.

        Returns:
            Result: An object containing the status code, message, and data from the response if successful.
            requests.Response: The raw response object if jsonify is False.
        """
        full_url = self.url + endpoint
        headers = {"x-api-key": self._api_key}
        # fix for when ep_params is empty
        log_line_pre = (
            f"method={http_method}, "
            + f"url={full_url}, params={str(ep_params).replace('{', '[').replace('}', ']')}"
        )
        log_line_post = ", ".join(
            (log_line_pre, "success={}, status_code={}, message={}")
        )

        # log request and perform HTTP Request catching exceptions and re-raising
        try:
            self._logger.debug(msg=log_line_pre)
            response = requests.request(
                method=http_method,
                url=full_url,
                verify=self._ssl_verify,
                headers=headers,
                params=ep_params,
                json=data,
                files=files,
            )
        except requests.exceptions.RequestException as e:
            self._logger.error(msg=str(e))
            raise LabEngineException(f"Request Failed: {e}")

        if not jsonify:
            return response

        # Deserialize response into python object
        try:
            data_out = response.json()
        except (ValueError, JSONDecodeError) as e:
            if response is FileResponse:
                data_out = response
            else:
                self._logger.error(msg=log_line_post.format(False, None, e))
                raise LabEngineException(f"Bad JSON in response: {e}")

        # if sucess return result else raise exception
        is_success = 299 >= response.status_code >= 200
        log_line = log_line_post.format(
            is_success, response.status_code, response.reason
        )
        if is_success:
            self._logger.debug(msg=log_line)
            return Result(response.status_code, message=response.reason, data=data_out)
        self._logger.error(msg=log_line)
        raise LabEngineException(
            f"{response.status_code}: {response.reason}, {response.text}"
        )

    def get(
        self, endpoint: str, ep_params: Dict = None, data: Dict = None, jsonify=True
    ) -> Result | requests.Response:
        """
        Performs a GET request to the specified endpoint.

        Args:
            endpoint (str): The API endpoint to send the GET request to.
            ep_params (Dict, optional): Query parameters for the endpoint. Defaults to None.
            data (Dict, optional): JSON body to include in the request. Defaults to None.
            jsonify (bool, optional): If True, parses the response as JSON. If False, returns the raw response.

        Returns:
            Result: An object containing the status code, message, and data from the response if successful.
            requests.Response: The raw response object if jsonify is False.
        """
        return self._do(
            http_method="GET",
            endpoint=endpoint,
            ep_params=ep_params,
            data=data,
            jsonify=jsonify,
        )

    def put(self, endpoint: str, ep_params: Dict = None, data: Dict = None) -> Result:
        """
        Performs a PUT request to the specified endpoint.

        Args:
            endpoint (str): The API endpoint to send the PUT request to.
            ep_params (Dict, optional): Query parameters for the endpoint. Defaults to None.
            data (Dict, optional): JSON body to include in the request. Defaults to None.

        Returns:
            Result: An object containing the status code, message, and data from the response if successful.
        """
        return self._do(
            http_method="PUT", endpoint=endpoint, ep_params=ep_params, data=data
        )

    def post(self, endpoint: str, ep_params: Dict = None, data: Dict = None) -> Result:
        """
        Performs a POST request to the specified endpoint.

        Args:
            endpoint (str): The API endpoint to send the POST request to.
            ep_params (Dict, optional): Query parameters for the endpoint. Defaults to None.
            data (Dict, optional): JSON body to include in the request. Defaults to None.

        Returns:
            Result: An object containing the status code, message, and data from the response if successful.
        """
        return self._do(
            http_method="POST", endpoint=endpoint, ep_params=ep_params, data=data
        )

    def patch(
        self, endpoint: str, ep_params: Dict = None, data: Dict = None, files=None
    ) -> Result:
        """
        Performs a PATCH request to the specified endpoint.

        Args:
            endpoint (str): The API endpoint to send the PATCH request to.
            ep_params (Dict, optional): Query parameters for the endpoint. Defaults to None.
            data (Dict, optional): JSON body to include in the request. Defaults to None.
            files (Any, optional): Files to upload with the request. Defaults to None.

        Returns:
            Result: An object containing the status code, message, and data from the response if successful.
        """
        return self._do(
            http_method="PATCH",
            endpoint=endpoint,
            ep_params=ep_params,
            data=data,
            files=files,
        )

    def delete(
        self, endpoint: str, ep_params: Dict = None, data: Dict = None
    ) -> Result:
        """
        Performs a DELETE request to the specified endpoint.

        Args:
            endpoint (str): The API endpoint to send the DELETE request to.
            ep_params (Dict, optional): Query parameters for the endpoint. Defaults to None.
            data (Dict, optional): JSON body to include in the request. Defaults to None.

        Returns:
            Result: An object containing the status code, message, and data from the response if successful.
        """
        return self._do(
            http_method="DELETE", endpoint=endpoint, ep_params=ep_params, data=data
        )
