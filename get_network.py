import json
from napalm import get_network_driver
from yaml import safe_load
import urllib3

# Disable warnings
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


class NetBot:
    """
    Defining a class called NetBot
    """

    USERNAME = "admin"
    PASSWORD = "admin"
    NET_BLOCK = {
        "type": "section",
        "text": {
            "type": "mrkdwn",
            "text": (
                "Getting interface information for device :slightly_smiling_face:"
            ),
        },
    }

    def __init__(self, channel, device_name):
        """
        constructor for class
        """
        self.channel = channel
        self.device_name = device_name

    def send_help(self):
        """
        Sending all the help
        """
        with open("README.md", "r") as reader:
            readme = reader.read()
        return {
            "channels": self.channel,
            "filename": "README.md",
            "filetype": "markdown",
            "content": readme,
        }

    def _get_facts(self):
        """
        Method that will retrieve host facts
        """
        with open("hosts.yaml", "r") as handle:
            host_root = safe_load(handle)

        driver = get_network_driver(host_root[f"{self.device_name}"]["platform"])
        conn = driver(
            hostname=host_root[f"{self.device_name}"]["mgmt"],
            username=self.USERNAME,
            password=self.PASSWORD,
        )
        conn.open()
        facts = conn.get_interfaces()
        my_file = json.dumps(facts, indent=2)
        return my_file

    def get_message_payload(self):
        """
        Method that uses the block version of posting messages
        and uses the class attribute of NET_BLOCK for generic message
        """
        return {"channel": self.channel, "blocks": [self.NET_BLOCK]}

    def get_file_payload(self):
        """
        Method used to post files from data gathered on device
        """
        return {
            "channels": self.channel,
            "filetype": "javascript",
            "content": self._get_facts(),
            "filename": f"{self.device_name}-interfaces.json",
        }
