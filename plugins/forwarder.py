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

        if msg.in_thread:
            await self.forward_threaded_message(msg)
        else:
            await self.forward_new_message(msg)

    async def forward_threaded_message(self, msg):
        message_link = await self.web_client.chat_getPermalink(
            channel=msg.channel.id,
            message_ts=msg.ts
        )
        forwarded_message = await self.say(
            channel=self.settings['FORWARDER_INBOX'],
            text=f"Thread mention: {message_link['permalink']}"
        )
        forwarded_link = await self.web_client.chat_getPermalink(
            channel=forwarded_message['channel'],
            message_ts=forwarded_message['ts']
        )

        await msg.say(text=f"{forwarded_link['permalink']}", thread_ts=msg.ts)

    async def forward_new_message(self, msg):
        forwarded_message = await self.say(
            channel=self.settings['FORWARDER_INBOX'],
            text=msg.text
        )
        link = await self.web_client.chat_getPermalink(
            channel=forwarded_message['channel'],
            message_ts=forwarded_message['ts']
        )

        await msg.say(text=f"This message has been sent to {self.settings['FORWARDER_INBOX']}. Please visit the link for further coordination: {link['permalink']}", thread_ts=msg.ts)
