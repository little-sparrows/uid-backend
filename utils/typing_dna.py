from typing import Optional
from enum import Enum

from pydantic import BaseModel

from aiohttp import ClientSession
from aiohttp.helpers import BasicAuth

from config import environment


class Action(str, Enum):
    enroll = 'enroll'
    verify = 'verify'
    verify_and_enroll = 'verify;enroll'


class BaseTDNAResponse(BaseModel):
    class Config:
        use_enum_values = True


class Responses:
    class Error(BaseTDNAResponse):
        name: str
        message: str
        message_code: int
        status: int

    class Auto(BaseTDNAResponse):
        status: int
        message: str
        message_code: int
        action: Action
        enrollment: bool
        result: bool
        high_confidence: bool
        custom_field: Optional[str]

    class CheckUser(BaseTDNAResponse):
        message: str
        message_code: int
        success: bool
        count: int
        mobilecount: int
        type: str
        status: int
        custom_field: Optional[str]

    class SaveTypingPattern(BaseTDNAResponse):
        message: str
        message_code: int
        success: bool
        status: int
        custom_field: Optional[str]

    class VerifyTypingPattern(BaseTDNAResponse):
        message: str
        message_code: int
        success: bool
        result: bool
        confidence: int
        net_score: int
        device_similarity: int
        score: int
        positions: list[int]
        previous_samples: int
        compared_samples: int
        status: int
        action: Action
        custom_field: Optional[str]
        confidence_interval: Optional[int]  # deprecated


class TypingDNA:
    _base_url = 'https://api.typingdna.com'

    def __init__(self,
                 api_key: str,
                 api_secret: str):

        self._api_key = api_key
        self._api_secret = api_secret

    @property
    def _cs(self):  # client session
        return ClientSession(
            base_url=self._base_url,
            auth=BasicAuth(self._api_key, self._api_secret)
        )

    async def auto(
            self,
            user_identifier: str,
            typing_patterns: list[str],
            custom_field: Optional[str] = None
    ) -> Responses.Auto:

        typing_patterns = ','.join(typing_patterns)

        dict_data = {
            "tp": typing_patterns,
        }

        if custom_field is not None:
            dict_data.update({"custom_field": custom_field})

        async with self._cs as cs:
            response = await cs.post(
                f'/auto/{user_identifier}',
                json=dict_data
            )
            status_code = response.status
            data = await response.json()

        if status_code // 100 == 2:
            result = Responses.Auto.parse_obj(data)
        else:
            result = Responses.Error.parse_obj(data)

        return result

    async def save_typing_pattern(
            self,
            user_identifier: str,
            typing_pattern: str,
            custom_field: Optional[str] = None,
    ) -> Responses.SaveTypingPattern:

        dict_data = {
            "tp": typing_pattern,
        }

        if custom_field is not None:
            dict_data.update({"custom_field": custom_field})

        async with self._cs as cs:
            response = await cs.post(
                f'/save/{user_identifier}',
                json=dict_data
            )
            status_code = response.status
            data = await response.json()

        if status_code // 100 == 2:
            result = Responses.SaveTypingPattern.parse_obj(data)
        else:
            result = Responses.Error.parse_obj(data)

        return result

    async def verify_typing_pattern(
            self,
            user_identifier: str,
            typing_patterns: list[str],
            quality: int,
            device_similarity_only: bool = None,
            position_only: bool = None,
            custom_field: Optional[str] = None,
    ) -> Responses.SaveTypingPattern:

        typing_patterns = ','.join(typing_patterns)

        dict_data = {
            "tp": typing_patterns,
            "quality": quality,
        }

        if device_similarity_only is not None:
            dict_data.update({"device_similarity_only": device_similarity_only})
        if position_only is not None:
            dict_data.update({"position_only": position_only})
        if custom_field is not None:
            dict_data.update({"custom_field": custom_field})

        async with self._cs as cs:
            response = await cs.post(
                f'/verify/{user_identifier}',
                json=dict_data
            )
            status_code = response.status
            data = await response.json()

        if status_code // 100 == 2:
            result = Responses.SaveTypingPattern.parse_obj(data)
        else:
            result = Responses.Error.parse_obj(data)

        return result


typing_dna = TypingDNA(
    api_key=environment.typing_dna_api_key,
    api_secret=environment.typing_dna_api_secret,
)


def get_current_dna_api_key() -> str:
    return typing_dna._api_key  # noqa
