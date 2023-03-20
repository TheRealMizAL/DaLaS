# DaLaS
## Fully customizable asynchronous Donation Alerts API

## Install:
> pip install dalas

## Before you start

1) Create your OAuth API App here: https://www.donationalerts.com/application/clients
2) Check the docs: https://www.donationalerts.com/apidoc

### Hello world:
```python
import asyncio

from dalas import Dalas, Scopes, token

dalas = Dalas(token.Token(client_id, Scopes.ALL)) # get client_ip from you OAuth API App
asyncio.run(dalas.api.send_custom_alerts(message='test'))
```


And then donations go **BRRRR**!