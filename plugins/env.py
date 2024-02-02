import os

from utilities.github_http import GitHubHTTP
from utilities.env_slack_responses import build_env_reply
from machine.plugins.base import MachineBasePlugin
from machine.plugins.decorators import command, required_settings
from structlog.stdlib import get_logger

logger = get_logger(__name__)
client = GitHubHTTP(agent="bw-env-bot")

@required_settings(["GITHUB_TOKEN"])

class EnvBot(MachineBasePlugin):
    @command("/env")
    async def env_handler(self, command: command):

        logger.info(f"Received {command.command}: {command.text} from {command.sender.name} in {command.channel.name}")

        cmd = command.text.split(" ")[0]

        if "list" in cmd:
            try:
                gh_environments = [env["name"] for env in client.get("https://api.github.com/repos/bitwarden/server/environments")["environments"] if "Cloud" in env["name"]]

                env_block = build_env_reply(gh_environments)

                await command.say("Bitwarden Environments", blocks=env_block)
            except Exception as e:
                logger.error(f"Error: {e}")
                await command.say(f"Error: {e}")
                return
        else:
            await command.say(f"Unknown command: {cmd}")
            return