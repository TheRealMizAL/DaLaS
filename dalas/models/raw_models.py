from typing import List

from .base_models import BaseModel, Meta, Links
from .data_models import UserInfo, Donation, SendCustomAlerts, CreateMerchandise, UpdateMerchandise, ChannelSubResponse, \
    CentrifugoResponse

__all__ = ("UserInfoRaw",
           "DonationAlertsListRaw",
           "SendCustomAlertsRaw",
           "CreateMerchandiseRaw",
           "UpdateMerchandiseRaw",
           "ChannelSubRaw",
           "CentrifugoResponseRaw")


class UserInfoRaw(BaseModel):
    data: UserInfo


class DonationAlertsListRaw(BaseModel):
    links: Links
    meta: Meta
    data: List[Donation]


class SendCustomAlertsRaw(BaseModel):
    data: SendCustomAlerts


class CreateMerchandiseRaw(BaseModel):
    data: CreateMerchandise


class UpdateMerchandiseRaw(BaseModel):
    data: UpdateMerchandise


class ChannelSubRaw(BaseModel):
    id: int
    result: ChannelSubResponse


class CentrifugoResponseRaw(BaseModel):
    result: CentrifugoResponse
