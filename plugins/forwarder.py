import re

from machine.plugins.base import MachineBasePlugin
from machine.plugins.decorators import listen_to, required_settings
from structlog.stdlib import get_logger

logger = get_logger(__name__)

@required_settings(['FORWARDER_INBOX'])
class ResponderBot(MachineBasePlugin):

    @listen_to(regex=rf"<@U01NJ9RDQ2D>")
    async def forward_message(self, msg):
        logger.info(msg.text)
        forwarded_msg = await self.say(
            channel=self.settings['FORWARDER_INBOX'],
            text=msg.text
        )
        link = await self.web_client.chat_getPermalink(
            channel=forwarded_msg['channel'],
            message_ts=forwarded_msg['ts']
        )

        await msg.say(text=f"{link['permalink']}", thread_ts=msg.ts)
