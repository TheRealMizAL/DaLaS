from abc import ABC, abstractmethod
import enum


class BaseValidator(ABC):

    @abstractmethod
    async def request_validator(self, request):
        pass

    @abstractmethod
    async def response_validator(self, response):
        pass


class DefaultValidator(BaseValidator):

    async def response_validator(self, response: dict):
        response_copy = response.copy()
        for k, v in response.items():
            if k.startswith('is_') and isinstance(v, int):
                response_copy[k] = bool(v)
            elif k in ('from',
                       'to'):  # we need this horrible piece of shit bc name "from" reserved, but we have "from" in "links". "to" renamed just for compatibility
                del response_copy[k]
                response_copy[f'{k}_index'] = v
            elif isinstance(v, dict):
                response_copy[k] = await self.response_validator(v)
            elif isinstance(v, list):
                values = []
                for i in range(len(v)):
                    values.append(await self.response_validator(v[i]))
                response_copy[k] = values

        return response_copy

    async def request_validator(self, request: dict):
        request_copy = request.copy()
        for k, v in request.items():

            if isinstance(k, enum.Enum):
                del request_copy[k]
                k = k.value
                request_copy[k] = v
            elif k == 'self' or k.startswith('__') or not v:
                del request_copy[k]

            elif isinstance(v, bool):
                request_copy[k] = int(v)
            elif isinstance(v, enum.Enum):
                request_copy[k] = v.value
            elif isinstance(v, dict):
                request_copy[k] = await self.request_validator(v)
        return request_copy
