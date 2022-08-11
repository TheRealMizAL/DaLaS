import enum
from pydantic import BaseModel

try:
    from typing import Literal
except ImportError:
    from typing_extensions import Literal


class Scopes:
    OAUTH_USER_SHOW = 'oauth-user-show'
    OUATH_DONATION_SUBSCRIBE = 'oauth-donation-subscribe'
    OAUTH_DONATION_INDEX = 'oauth-donation-index'
    OAUTH_CUSTOM_ALERT_STORE = 'oauth-custom_alert-store'
    OAUTH_GOAL_SUBSCRIBE = 'oauth-goal-subscribe'
    OAUTH_POLL_SUBSCRIBE = 'oauth-poll-subscribe'

    ALL = ' '.join([OAUTH_POLL_SUBSCRIBE, OAUTH_GOAL_SUBSCRIBE, OAUTH_CUSTOM_ALERT_STORE, OUATH_DONATION_SUBSCRIBE,
                    OAUTH_DONATION_INDEX, OAUTH_USER_SHOW])


class Locales(enum.Enum):
    Belarusian = 'be_BY'
    German = 'de_DE'
    English_US = 'en_US'
    Spanish = 'es_ES'
    Spanish_US = 'es_US'
    Estonian = 'et_EE'
    French = 'fr_FR'
    Hebrew = 'he_HE'
    Italian = 'it_IT'
    Georgian = 'ka_GE'
    Kazakh = 'kk_KZ'
    Korean = 'ko_KR'
    Latvian = 'lv_LV'
    Polish = 'pl_PL'
    Portuguese_BR = 'pt_BR'
    Russian = 'ru_RU'
    Swedish = 'sv_SE'
    Turkish = 'tr_TR'
    Ukrainian = 'uk_UA'
    Chinese = 'zh_CN'


class InputCurrencies(enum.Enum):
    EURO = 'EUR'
    US_DOLLAR = 'USD'
    RU_RUBLE = 'RUB'
    REAL = 'BRL'
    LIRA = 'TRY'


class OutputCurrencies(enum.Enum):
    EURO = 'EUR'
    US_DOLLAR = 'USD'
    RU_RUBLE = 'RUB'
    REAL = 'BRL'
    LIRA = 'TRY'
    BU_RUBLE = 'BYN'
    TENGE = 'KZT'
    HRYVNIA = 'UAH'


class CentrifugoChannel(enum.Enum):
    NEW_DONATION_ALERTS = "$alerts:donation"
    DONATION_GOALS_UPDATES = "$goals:goal"
    POLLS_UPDATES = "$polls:poll"


class TokenRequest(BaseModel):
    client_id: int
    redirect_uri: str
    response_type: Literal["code", "token"]
    scope: str


class TokenResponse(BaseModel):
    token_type: str
    expires_in: int
    access_token: str
    refresh_token: str
