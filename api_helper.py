from loguru import logger
import requests

class APIHelper:
    def __init__(self, base_url):
        self.base_url = base_url

    def make_api_request(self, endpoint, method="GET", headers=None, **kwargs):
        url = f"{self.base_url}{endpoint}"
        headers = headers or {}

        if method == "GET":
            response = requests.get(url, headers=headers, **kwargs)

        elif method == "POST":
            response = requests.post(url, headers=headers, **kwargs)

        else:
            raise ValueError("Unsupported HTTP method")

        logger.info(response.text)
        response.raise_for_status()
        return response.json()