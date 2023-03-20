from abc import ABC

import aiohttp
from loguru import logger
from .validators import BaseValidator

try:
    from orjson import orjson as json
except ImportError:
    import json


class BaseRequester(ABC):
    def __init__(self, base_url: str, token: str, validator: BaseValidator):
        self.__BASE_URL = base_url
        self.__token = token
        self.validator = validator

    async def request_api(self, method_name: str, method: str = 'GET', **kwargs):
        raise NotImplementedError()


class HTTPRequester(BaseRequester):
    def __init__(self, base_url: str,
                 token: str,
                 validator: BaseValidator):
        super().__init__(base_url, token, validator)
        self.__BASE_URL = base_url
        self.__token = token
        self.validator = validator

    async def request_api(self, method_name: str, method: str = 'GET', **kwargs):
        async with aiohttp.ClientSession(connector=aiohttp.TCPConnector(ssl=False)) as session:
            async with session.request(url=self.__BASE_URL + method_name,
                                       method=method, data=json.dumps(kwargs),
                                       headers={"Authorization": f"Bearer {self.__token}",
                                                "Content-Type": "application/json"}) as request:
                response = await request.json()
                logger.debug(f'Requesting "{method_name}" with {kwargs} returned: {response}')

        response = await self.validator.response_validator(response)
        logger.debug("API response was validated")
        return response
