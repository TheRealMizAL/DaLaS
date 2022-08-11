from typing import Optional, Union
import datetime

import pydantic

from ..types import InputCurrencies


class BaseModel(pydantic.BaseModel):
    class Config:
        arbitrary_types_allowed = True


class Links(BaseModel):
    first: str
    last: str
    prev: Optional[str]
    next: Optional[str]


class Meta(BaseModel):
    current_page: int
    from_index: int  # originally named "from"
    last_page: int
    path: str
    per_page: int
    to_index: int  # originally named "to"
    total: int


class Merchant(BaseModel):
    identifier: str
    name: str


class Title:
    Belarusian: Optional[str]
    German: Optional[str]
    English_US: Optional[str]
    Spanish: Optional[str]
    Spanish_US: Optional[str]
    Estonian: Optional[str]
    French: Optional[str]
    Hebrew: Optional[str]
    Italian: Optional[str]
    Georgian: Optional[str]
    Kazakh: Optional[str]
    Korean: Optional[str]
    Latvian: Optional[str]
    Polish: Optional[str]
    Portuguese_BR: Optional[str]
    Russian: Optional[str]
    Swedish: Optional[str]
    Turkish: Optional[str]
    Ukrainian: Optional[str]
    Chinese: Optional[str]


class PayinSystem(BaseModel):
    title: str


class BaseMerch(BaseModel):
    id: int
    merchant: Merchant
    identifier: str
    title: Title
    is_active: bool
    is_percentage: bool
    currency: InputCurrencies
    price_user: Union[float, int]
    price_service: Union[float, int]
    url: Optional[str]
    img_url: Optional[str]
    end_at: datetime.datetime
