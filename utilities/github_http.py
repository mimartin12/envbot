import os
import urllib3
import json
from structlog.stdlib import get_logger

logger = get_logger(__name__)

class GitHubHTTP:
    def __init__(self, agent) -> None:
        self.agent = agent
        if self.agent is None:
            self.agent = "bw-automated-bot"

        self.headers = {"user-agent": self.agent}

        if os.getenv("GITHUB_TOKEN", None):
            self.headers["Authorization"] = f"Token {os.environ['GITHUB_TOKEN']}"

        self.http = urllib3.PoolManager()

    def get(self, url):
        try:
            resp = json.loads(
                self.http.request("GET", url, headers=self.headers).data.decode("utf-8")
            )
            return resp
        except Exception as e:
            logger.error(f"Error: {e}")
            return e

