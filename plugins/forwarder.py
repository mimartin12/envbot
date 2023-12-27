import os
import re
from collections import namedtuple

from machine.plugins.base import MachineBasePlugin
from machine.plugins.decorators import listen_to, required_settings
from structlog.stdlib import get_logger

logger = get_logger(__name__)

LISTEN_ID_REGEX = rf"<@{os.environ['FORWARDER_LISTEN_ID']}>"


@required_settings(["FORWARDER_INBOX", "FORWARDER_LISTEN_ID"])
class ResponderBot(MachineBasePlugin):

    @listen_to(regex=LISTEN_ID_REGEX)
    async def forward_message(self, msg):
        logger.info(msg.text)

        if msg.in_thread:
            await self.__forward_threaded_message(msg)
        else:
            await self.__forward_new_message(msg)

    async def __forward_message(self, fmsg_text):
        fmsg = await self.say(
            channel=self.settings["FORWARDER_INBOX"],
            text=fmsg_text,
        )
        link = await self.web_client.chat_getPermalink(
            channel=fmsg["channel"],
            message_ts=fmsg["ts"]
        )

        return fmsg, link

    async def __forward_threaded_message(self, msg):
        msg_link = await self.web_client.chat_getPermalink(
            channel=msg.channel.id, message_ts=msg.ts
        )

        fmsg, link = await self.__forward_message(f"Thread mention: {msg_link['permalink']}")

        await msg.say(
            text=f"{link['permalink']}",
            thread_ts=msg.ts
        )

    async def __forward_new_message(self, msg):
        fmsg, link = await self.__forward_message(msg.text)

        await msg.say(
            text=(
                f"This message has been sent to {self.settings['FORWARDER_INBOX']}."
                f"Please visit the link for further coordination: {link['permalink']}"
            ),
            thread_ts=msg.ts,
        )

