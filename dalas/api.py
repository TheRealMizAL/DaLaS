from typing import Union, List, Optional, Dict

from dalas.http_requests import HTTPRequester, BaseRequester
from dalas.models.data_models import UserInfo, Donation, SendCustomAlerts
from dalas.models.raw_models import UserInfoRaw, DonationAlertsListRaw, SendCustomAlertsRaw
from dalas.types import Locales
from dalas.validators import BaseValidator, DefaultValidator

MerchTitle = Dict[Union[str, Locales], str]


class API:

    def __init__(self,
                 api_requester: Optional[BaseRequester],
                 validator: BaseValidator = DefaultValidator(),
                 raw_responses: bool = False):
        self.__request_api = api_requester.request_api
        self.validator = validator
        self.raw_responses = raw_responses

    async def user(self) -> Union[UserInfoRaw, UserInfo]:
        response: UserInfoRaw = UserInfoRaw(**(await self.__request_api('user/oauth')))
        if self.raw_responses:
            return response
        return response.data

    async def donation_alerts_list(self) -> Union[DonationAlertsListRaw, List[Donation]]:
        response: DonationAlertsListRaw = DonationAlertsListRaw(**(await self.__request_api('alerts/donations')))
        if self.raw_responses:
            return response
        return response.data

    async def send_custom_alerts(self,
                                 external_id: Optional[str] = None,
                                 header: Optional[str] = None,
                                 message: Optional[str] = None,
                                 is_shown: Optional[Union[int, bool]] = None,
                                 image_url: Optional[str] = None,
                                 sound_url: Optional[str] = None,
                                 **kwargs) -> Union[SendCustomAlerts, SendCustomAlertsRaw]:
        params = await self.validator.request_validator(locals())
        response: SendCustomAlertsRaw = SendCustomAlertsRaw(
            **(await self.__request_api('custom_alert', method='POST', **params)))
        if self.raw_responses:
            return response
        return response.data

    # todo: finish when possible
    # async def create_merch(self,
    #                        merchant_identifier: str,
    #                        merchandise_identifier: str,
    #                        title: MerchTitle,
    #                        currency: Union[str, InputCurrencies],
    #                        price_user: Union[float, int],
    #                        price_service: Union[float, int],
    #                        signature: str,
    #                        end_at_ts: int = int(time.time()),
    #                        is_active: Union[int, bool] = False,
    #                        is_percentage: Union[int, bool] = False,
    #                        url: Optional[str] = None,
    #                        img_url: Optional[str] = None):
    #     params = await self.validator.request_validator(locals())
    #     return await self.__request_api('merchandise', method='POST', **params)
    #
    # async def update_merch(self,
    #                        id: str,
    #                        merchant_identifier: Optional[str] = None,
    #                        merchandise_identifier: Optional[str] = None,
    #                        title: Optional[Union[MerchTitle, dict]] = None,
    #                        is_active: Optional[Union[bool, int]] = None,
    #                        is_percentage: Optional[Union[bool, int]] = None,
    #                        currency: Optional[Union[InputCurrencies, str]] = None,
    #                        price_user: Union[float, int] = None,
    #                        price_service: Union[float, int] = None,
    #                        url: Optional[str] = None,
    #                        img_url: Optional[str] = None,
    #                        end_at_ts: Optional[int] = int(time.time()),
    #                        signature: Optional[str] = None):
    #
    #     params = await self.validator.request_validator(locals())
    #     return await self.__request_api(f'merchandise/{id}', method='PUT', **params)
    #
    # async def send_sale_alerts(self,
    #                            user_id: int,
    #                            external_id: str,
    #                            merchant_identifier: str,
    #                            merchandise_identifier: str,
    #                            amount: Union[float, int],
    #                            currency: Union[str, InputCurrencies],
    #                            signature: str,
    #                            bought_amount: int = 1,
    #                            username: Optional[str] = None,
    #                            message: Optional[str] = None):
    #
    #     params = await self.validator.request_validator(locals())
    #     return await self.__request_api('merchandise_sale', method='POST', **params)
