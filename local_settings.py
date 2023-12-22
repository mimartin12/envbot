import os

from dotenv import load_dotenv

load_dotenv()

ALIASES='!'
LOGLEVEL="INFO"
SLACK_APP_TOKEN = os.getenv("SLACK_APP_TOKEN")
SLACK_BOT_TOKEN = os.getenv("SLACK_BOT_TOKEN")

FORWARDER_INBOX = "#inbox-joseph"


PLUGINS = [
    "machine.plugins.builtin.general.HelloPlugin",
    "plugins.forwarder.ResponderBot"
]
