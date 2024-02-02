import os

from dotenv import load_dotenv

load_dotenv()

ALIASES = "!"
LOGLEVEL = "INFO"
SLACK_APP_TOKEN = os.getenv("SLACK_APP_TOKEN")
SLACK_BOT_TOKEN = os.getenv("SLACK_BOT_TOKEN")

FORWARDER_INBOX = os.getenv("FORWARDER_INBOX")
FORWARDER_LISTEN_ID = os.getenv("FORWARDER_LISTEN_ID")

GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")


PLUGINS = [
    "plugins.env.EnvBot",
    # "machine.plugins.builtin.general.HelloPlugin",
    # "plugins.forwarder.ResponderBot",
]
