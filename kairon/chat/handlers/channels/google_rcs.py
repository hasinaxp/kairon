import logging
from typing import Dict, Text, Any, List, Optional

from rasa.core.channels.channel import InputChannel, UserMessage, OutputChannel
from rasa.shared.constants import INTENT_MESSAGE_PREFIX
from rasa.shared.core.constants import USER_INTENT_RESTART
from starlette.requests import Request

from kairon.chat.converters.channels.response_factory import ConverterFactory
from kairon.chat.handlers.channels.base import ChannelHandlerBase
from kairon.shared.chat.processor import ChatDataProcessor
from kairon.shared.constants import ChannelTypes
from kairon.shared.models import User
from kairon.chat.agent_processor import AgentProcessor
from kairon import Utility
import json
import aiohttp
import base64
import hashlib
import hmac

from kairon.shared.channels.rcs_business_messaging import rbm_service
from kairon.shared.channels.rcs_business_messaging import messages

logger = logging.getLogger(__name__)

'''
from rcs_business_messaging import rbm_service
from rcs_business_messaging import messages

# Create media file attachment
file_message = messages.FileMessage('http://www.google.com/logos/doodles/2015/googles-new-logo-5078286822539264.3-hp2x.gif')

messages.MessageCluster().append_message(file_message).send_to_msisdn('+12223334444')

'''

class RCSOutput(OutputChannel):
    """Output channel for RCS."""

    @classmethod
    def name(cls) -> Text:
        return "rcs"

    def __init__(self, certificate: str) -> None:
        self.certificate = certificate
        self.rcs = rbm_service.RCSService(certificate)

    async def send_text_message(self, recipient_id: Text, text: Text, **kwargs: Any) -> None:
        text_msg = messages.TextMessage(text)
        msg_cluster = messages.MessageCluster(self.rcs)
        msg_cluster.append_message(text_msg).send_to_msisdn(self.rcs, recipient_id)


class RCSHandler(InputChannel, ChannelHandlerBase):
    """RCS input channel."""
    def __init__(self, bot: Text, user: User, request: Request):
        self.bot = bot
        self.user = user
        self.request = request

    async def handle_message(self):
        google_rcs = ChatDataProcessor.get_channel_config(ChannelTypes.GOOGLE_RCS.value, self.bot, mask_characters=False)

        print('message received')
        req_data:dict = await self.request.json()
        print(req_data)

        #TODO: verify client token if required (not necessary for now ut its just for better security)



        print(google_rcs['config'])


        output_channel = RCSOutput(google_rcs['config']['certificate'])
        output_channel.rcs.invite_tester('+9108240258440')
        # await output_channel.send_text_message('+918240258440', 'Hello, world!')
        print('message sent')
        if 'secret' in req_data:
            return req_data.get('secret')

    @staticmethod
    async def process_message(bot: str, user_message: UserMessage):
        await AgentProcessor.get_agent(bot).handle_message(user_message)


