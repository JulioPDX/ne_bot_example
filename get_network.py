from napalm import get_network_driver
from yaml import safe_load
import json


class NetBot:
    """
    Main stuff to format messages
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

    def __init__(self, channel):
        """
        self module
        """
        self.channel = channel

    def _get_facts(self):
        """
        function that will retrieve host facts
        """
        with open("hosts.yaml", "r") as handle:
            host_root = safe_load(handle)

        driver = get_network_driver(host_root["R1"]["platform"])
        conn = driver(
            hostname=host_root["R1"]["mgmt"],
            username=self.USERNAME,
            password=self.PASSWORD,
        )
        conn.open()
        # facts = conn.get_facts()
        facts = conn.get_interfaces()
        with open("./json/data.txt", "w") as outfile:
            json.dump(facts, outfile, indent=2)
        with open("./json/data.txt", "r") as reader:
            myfile = reader.read()
        # return ({"type": "section", "text": {"type": "mrkdwn", "text": text}},)
        return myfile

    def get_message_payload(self):
        """
        Function that uses the block version of posting messages
        """
        # return {"channel": self.channel, "blocks": [self.NET_BLOCK, *self._get_facts()]}
        return {"channel": self.channel, "blocks": [self.NET_BLOCK]}

    def get_file_payload(self):
        """
        Function used to post files from data gathered on device
        """
        return {
            "channels": self.channel,
            "filetype": "javascript",
            "content": self._get_facts(),
        }
