import urllib
from slack_sdk.models.blocks import RichTextBlock, DividerBlock
from structlog.stdlib import get_logger

logger = get_logger(__name__)

def build_env_reply(environments) -> list:
    """
    Build a Slack message with a list of Bitwarden Cloud environments.
    Applying the appropriate formatting for Slack.
    """
    title = [
        {
            "type": "rich_text_section",
            "elements": [
                {
                    "type": "text",
                    "text": "Bitwarden Cloud Environments",
                    "style": {
                        "bold": True,
                    }
                }
            ]
        }
    ]
    elements = []

    for env in environments:
        # Create url supported by Slack formatting
        env_url = "https://github.com/bitwarden/server/deployments/" + urllib.parse.quote(env)

        elements.append(
            {
                "type": "rich_text_section",
                "elements": [
                    {
                        "type": "text",
                        "text": env,
                        "style": {
                            "code": True
                        }
                    },
                    {
                        "type": "text",
                        "text": " "
					},
                    {
                        "type": "link",
                        "url": env_url,
                        "text": "view"
                    }
                ]
            }
        )

    return [
        RichTextBlock(elements=title),
        DividerBlock(),
        RichTextBlock(elements=elements)
        ]