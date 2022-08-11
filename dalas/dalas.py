import asyncio
from asyncio import AbstractEventLoop
from typing import Optional, Union

from .alerts import Alerts
from .api import API
from .http_requests import BaseRequester, HTTPRequester

try:
    from typing import Literal
except ImportError:
    from typing_extensions import Literal

from loguru import logger

from .token import Token
from .validators import BaseValidator, DefaultValidator


class Dalas:

    def __init__(self,
                 token: Union[str, Token],
                 client_id: int = None,
                 scopes: Optional[Union[str, list]] = None,
                 path: Optional[str] = None,
                 validator: BaseValidator = DefaultValidator(),
                 api_requester: Optional[BaseRequester] = None,
                 raw_responses: bool = False,
                 loop: Optional[AbstractEventLoop] = None):

        if token and any((client_id, scopes, path)):
            logger.warning('Token passed, other args are ignored.')

        if isinstance(token, str):
            self.__token = token
        elif isinstance(token, Token):
            self.__token = asyncio.run(token.key)
        else:
            raise ValueError("No token or token generator passed")

        self.loop = loop or asyncio.new_event_loop()
        self.__BASE_URL = 'https://www.donationalerts.com/api/v1/'

        self.api_requester = api_requester or HTTPRequester(self.__BASE_URL, self.__token, validator)

        self.api = API(self.api_requester, validator, raw_responses)
        self.alerts = Alerts(self.user, self.api_requester, self.loop)

    @property
    def user(self):
        return self.loop.run_until_complete(self.api.user())
