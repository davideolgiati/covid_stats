import requests
from urllib.parse import urljoin
from requests.adapters import Retry
from TimeoutHTTPAdapter import TimeoutHTTPAdapter


class ResilientHttpConnector:
    def __init__(self, base_url,
                 retry=3, backoff=1, retry_status=None,
                 retry_whitelist=None, timeout=0.30  # 30 seconds
                 ):
        # Connector
        connector = requests.Session()

        # Retry Config
        if retry_status is None:
            retry_status = [500, 404, 503]

        retries = Retry(total=retry,
                        backoff_factor=backoff,
                        status_forcelist=retry_status,
                        method_whitelist=retry_whitelist)

        # HTTP Layer configuration
        http_layer = TimeoutHTTPAdapter(max_retries=retries,
                                        timeout=timeout)

        # Connector setup
        connector.mount('http://', http_layer)
        connector.mount('https://', http_layer)
        connector.hooks["response"] = [
            lambda response, *args, **kwargs: response.raise_for_status()  # Exception on status_code != 200
        ]

        self.base_url = base_url
        self.connector = connector

    def get(self, path):
        self.connector.get(self.__full_url(path))

    def post(self, path, body):
        self.connector.post(self.__full_url(path), json=body)

    def __full_url(self, path):
        return urljoin(self.base_url, path)
