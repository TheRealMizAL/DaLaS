from typing import Union, Optional
from urllib.parse import urlencode
import time

import webbrowser
import yaml

from .http_requests import HTTPRequester
from .types import TokenRequest, TokenResponse
from .validators import DefaultValidator


class BaseToken:
    def __init__(self, path: str,
                 redirect_uri: str,
                 client_id: int,
                 response_type: str,
                 scope: Union[str, list]):
        self.path = path or '~/.donationalerts/secret.yaml'
        self.redirect_uri = redirect_uri
        self.client_id = client_id
        self.response_type = response_type
        self.scope = scope

    async def auth_request(self):
        data: TokenRequest = TokenRequest(client_id=self.client_id, redirect_uri=self.redirect_uri,
                                          response_type=self.response_type, scope=self.scope)
        url = 'https://www.donationalerts.com/oauth/authorize?' + urlencode(data.dict())
        webbrowser.open(url)

        return input(f'Copy {self.response_type} from url and paste here: ')

    @property
    async def key(self):
        raise NotImplementedError()


class AuthCode(BaseToken):
    def __init__(self,
                 path: str,
                 redirect_uri: str,
                 client_id: int,
                 scope: Union[str, list],
                 client_secret: str):
        super().__init__(path, redirect_uri, client_id, 'code', scope)
        self.client_secret = client_secret

    @property
    async def key(self):
        try:
            with open(self.path, 'r', encoding='utf-8') as file:
                token_response = TokenResponse(**yaml.load(file, yaml.Loader))
        except FileNotFoundError:
            token_response = await self.__get_token()
            with open(self.path, 'w', encoding='utf-8') as file:
                yaml.dump(token_response.dict(), file)
            return token_response.access_token

        if token_response.expires_in < int(time.time()):
            token_response = await self.__refresh_token(token_response.refresh_token)
            with open(self.path, 'w', encoding='utf-8') as file:
                yaml.dump(token_response.dict(), file)

        return token_response.access_token

    async def __get_token(self):
        code = await self.auth_request()
        response = await HTTPRequester('https://www.donationalerts.com/', '', DefaultValidator(), ).request_api(
            'oauth/token',
            'POST',
            grant_type='authorization_code',
            client_id=self.client_id,
            client_secret=self.client_secret,
            redirect_uri=self.redirect_uri,
            code=code)

        return TokenResponse(**response)

    async def __refresh_token(self, refresh_token: str):
        response = await HTTPRequester('https://www.donationalerts.com/', '', DefaultValidator()).request_api(
            'oauth/token',
            'POST',
            grant_type='refresh_token',
            refresh_token=refresh_token,
            client_id=self.client_id,
            client_secret=self.client_secret,
            scope=self.scope)

        return TokenResponse(**response)


class Implicit(BaseToken):

    def __init__(self,
                 path: str,
                 redirect_uri: str,
                 client_id: int,
                 scope: Union[str, list]):
        super().__init__(path, redirect_uri, client_id, 'token', scope)

    @property
    async def key(self):
        try:
            with open(self.path, 'r', encoding='utf-8') as file:
                return yaml.load(file, yaml.Loader)['access_token']
        except FileNotFoundError:
            token_response = await self.auth_request()
            with open(self.path, 'w', encoding='utf-8') as file:
                yaml.dump({'access_token': token_response}, file)
            return token_response


class Token:
    def __init__(self,
                 client_id: int,
                 scope: Union[str, list],
                 path: str = '~/.donationalerts/secret.yaml',
                 redirect_uri: str = '127.0.0.1:5000/',
                 response_type: str = 'token',
                 client_secret: Optional[str] = None):
        if response_type == 'token':
            self.token = Implicit(path, redirect_uri, client_id, scope)
        elif response_type == 'code':
            if not client_secret:
                raise ValueError('client_secret can\'t be None')
            self.token = AuthCode(path, redirect_uri, client_id, scope, client_secret)
        else:
            raise ValueError('Wrong response_type')

    @property
    async def key(self):
        return await self.token.key
