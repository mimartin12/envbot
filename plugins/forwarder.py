import os
import re
from collections import namedtuple

from machine.plugins.base import MachineBasePlugin
from machine.plugins.decorators import listen_to, required_settings
from machine.plugins.message import Message
from slack_sdk.web.async_slack_response import AsyncSlackResponse
from structlog.stdlib import get_logger

logger = get_logger(__name__)

LISTEN_ID_REGEX = rf"<@{os.environ['FORWARDER_LISTEN_ID']}>"


@required_settings(["FORWARDER_INBOX", "FORWARDER_LISTEN_ID"])
class ResponderBot(MachineBasePlugin):
    """Bot to automatically respond and forward pinged messages.

    Automatically redirect and forward messages to a central channel for a
    more simplistic support system for a team migrating to a single external
    communication channel. Gently remind people who have not yet fully learned
    the new process.
    """

    @listen_to(regex=LISTEN_ID_REGEX)
    async def forward_message(self, msg: Message) -> None:
        """Forward an individual or group ping to a specified inbox.

        Routes the ping depending on if the ping is in a thread or is the root
        message in a new thread.

        Args:
            msg: A message that contains text that matches the configured regex
        """
        logger.info(msg.text)

        if msg.in_thread:
            await self.__forward_threaded_message(msg)
        else:
            await self.__forward_new_message(msg)

    async def __forward_message(self, fmsg_text: str) -> tuple[AsyncSlackResponse, str]:
        """Generic message forwarder.

        Args:
            fmsg_text: Message text to forward.

        Returns:
            fmsg_resp: Response from Slack SDK from sending the message.
            link: The permalink to the message that was sent.
        """
        fmsg_resp = await self.say(
            channel=self.settings["FORWARDER_INBOX"],
            text=fmsg_text,
        )
        link = await self.web_client.chat_getPermalink(
            channel=fmsg_resp["channel"], message_ts=fmsg_resp["ts"]
        )

        return fmsg_resp, link

    async def __forward_threaded_message(self, msg: Message) -> None:
        """Forward a message from a thread.

        Args:
            msg: A message to foward a link to for a response in-place.
        """
        msg_link = await self.web_client.chat_getPermalink(
            channel=msg.channel.id, message_ts=msg.ts
        )

        _, link = await self.__forward_message(
            f"Thread mention: {msg_link['permalink']}"
        )

        await msg.say(text=f"{link['permalink']}", thread_ts=msg.ts)

    async def __forward_new_message(self, msg: Message) -> None:
        """Forward a new message in a channel.

        Args:
            msg: A message that needs to be forwarded.
        """
        _, link = await self.__forward_message(msg.text)

        await msg.say(
            text=(
                f"This message has been sent to {self.settings['FORWARDER_INBOX']}."
                f"Please visit the link for further coordination: {link['permalink']}"
            ),
            thread_ts=msg.ts,
        )
