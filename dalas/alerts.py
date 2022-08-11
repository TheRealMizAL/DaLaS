import asyncio
from asyncio import AbstractEventLoop
from typing import Optional, List, Callable, Union

import websockets
from loguru import logger

try:
    from orjson import orjson as json
except ImportError:
    import json

from dalas.types import CentrifugoChannel
from dalas.http_requests import BaseRequester
from dalas.models.data_models import UserInfo, NewAlertRaw
from dalas.models.raw_models import ChannelSubRaw


class FromFuncHandler:
    def __init__(self, handler: Callable, channel: CentrifugoChannel, blocking: bool = True):
        self.handler = handler
        self.channel = channel
        self.blocking = blocking

    async def check(self, event: NewAlertRaw):
        return event.result.channel.startswith(self.channel.value)


class Alerts:
    def __init__(self,
                 user: UserInfo,
                 api_requester: Optional[BaseRequester],
                 loop: Optional[AbstractEventLoop] = None):
        self.user = user
        self.__request_api = api_requester.request_api
        self.__WS_URL = 'wss://centrifugo.donationalerts.com/connection/websocket'

        self.loop = loop or asyncio.new_event_loop()

        self.handlers: List[FromFuncHandler] = []
        self.channels: List[CentrifugoChannel] = []

    async def subscribe(self):

        connect_json = json.dumps({'params': {'token': self.user.socket_connection_token},
                                   'id': self.user.id})

        async with websockets.connect(self.__WS_URL) as ws:
            await ws.send(connect_json)

            channel_response = ChannelSubRaw(**json.loads(await ws.recv()))

            api_response = await self.__request_api('centrifuge/subscribe',
                                                    method='POST',
                                                    channels=[f'{channel.value}_{channel_response.id}' for channel in
                                                              self.channels],
                                                    client=channel_response.result.client)
            for i in range(len(api_response["channels"])):
                await ws.send(json.dumps({
                    "params": {
                        "channel": api_response["channels"][i]["channel"],
                        "token": api_response["channels"][i]["token"]
                    },
                    "method": 1,
                    "id": self.user.id
                }))

            await self.listen_websocket(ws)

    async def listen_websocket(self, ws):
        logger.info('Websocket listener started')
        async for event in ws:
            js = json.loads(event)
            if 'id' in js.keys() or 'type' in js['result'].keys():
                continue

            event = NewAlertRaw(**js)
            logger.debug(f"Websocket received new event: {event.json()}")
            for handler in self.handlers:
                result = await handler.check(event)
                logger.debug(f'Handler {handler.handler.__name__} returned <{result}>')
                if result:
                    await handler.handler(event.result.data.data)
                if handler.blocking:
                    break
        logger.info('Websocket listener finished')

    def new_alert(self, channel: CentrifugoChannel, blocking=True):
        def decorator(func):
            self.handlers.append(
                FromFuncHandler(func, blocking=blocking, channel=channel)
            )
            self.channels.append(channel)
            return func

        return decorator
