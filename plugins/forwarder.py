import re

from machine.plugins.base import MachineBasePlugin
from machine.plugins.decorators import listen_to, required_settings
from structlog.stdlib import get_logger

logger = get_logger(__name__)

class JosephResponderBot(MachineBasePlugin):

    @required_settings(["INBOX_JOSEPH"])
    @listen_to(regex=r"Joseph")
    async def forward_message(self, msg):
        forwarded_msg = await self.say(
            channel=self.settings['INBOX_JOSEPH'],
            text=msg.text
        )
        link = await self.web_client.chat_getPermalink(
            channel=forwarded_msg['channel'],
            message_ts=forwarded_msg['ts']
        )

        await msg.say(text=f"{link['permalink']}", thread_ts=msg.ts)
