from typing import Optional, Union, List

import pydantic

try:
    from typing import Literal
except ImportError:
    from typing_extensions import Literal
import datetime

from pydantic import validator, ValidationError

from .base_models import BaseModel, PayinSystem, BaseMerch
from ..types import Locales, InputCurrencies

__all__ = ("UserInfo",
           "Donation",
           "SendCustomAlerts",
           "CreateMerchandise",
           "UpdateMerchandise",
           "SendSale",
           "ChannelSubResponse",
           "CentrifugoResponse")


class Alert(BaseModel):
    reason: Optional[str]


class UserInfo(BaseModel):
    id: int
    code: str
    name: str
    avatar: str
    email: str
    language: Locales
    socket_connection_token: str


class Donation(Alert):
    id: int
    name: str
    username: Optional[str]
    recipient_name: str
    message_type: str
    message: Optional[str]
    payin_system: PayinSystem
    amount: Union[int, float]
    currency: InputCurrencies
    amount_in_user_currency: Union[int, float]
    is_shown: bool
    created_at: datetime.datetime
    created_at_ts: Optional[int]
    shown_at: Optional[datetime.datetime]
    shown_at_ts: Optional[int]


class SendCustomAlerts(BaseModel):
    id: int
    external_id: Optional[str]
    header: Optional[str]
    message: Optional[str]
    image_url: Optional[str]
    sound_url: Optional[str]
    is_shown: bool
    created_at: datetime.datetime
    shown_at: Optional[datetime.datetime]


class CreateMerchandise(BaseMerch):
    pass


class UpdateMerchandise(BaseMerch):
    pass


class SendSale(BaseModel):
    id: int
    name: str
    external_id: str
    username: Optional[str]
    message: Optional[str]
    amount: int
    currency: InputCurrencies
    bought_amount: int
    is_shown: bool
    created_at: datetime.datetime
    shown_at: Optional[datetime.datetime]


class ChannelSubResponse(BaseModel):
    client: str
    version: str


class CentrifugoResponseInfo(BaseModel):
    user: str
    client: str


class CentrifugoResponseData(BaseModel):
    info: CentrifugoResponseInfo


class CentrifugoResponse(BaseModel):
    type: int
    channel: str
    data: CentrifugoResponseData


class GoalUpdate(Alert):
    id: int
    is_active: bool
    title: str
    currency: InputCurrencies
    start_amount: Union[int, float]
    raised_amount: Union[int, float]
    goal_amount: Union[int, float]
    started_at: datetime.datetime
    expires_in: Optional[datetime.datetime]


class PollOption(BaseModel):
    id: int
    title: str
    amount_value: Union[int, float]
    amount_percent: Union[int, float]
    is_winner: bool


class PollUpdate(Alert):
    id: int
    is_active: bool
    title: str
    allow_user_options: bool
    type: Literal["count", "sum"]
    options: List[PollOption]


class AlertData(pydantic.BaseModel):
    seq: int
    data: Union[Donation, PollUpdate, GoalUpdate]


class NewAlert(BaseModel):
    channel: str
    data: AlertData


class NewAlertRaw(BaseModel):
    result: NewAlert
