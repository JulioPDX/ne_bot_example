from napalm import get_network_driver
from yaml import safe_load


class NetBot:
    """
    Main stuff to format messages
    """

    USERNAME = "admin"
    PASSWORD = "admin"
    NET_BLOCK = {
        "type": "section",
        "text": {"type": "mrkdwn", "text": ("Getting interface information for device :slightly_smiling_face:")},
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
        text = f"```{facts}```"
        # text = "Hello World"

        return ({"type": "section", "text": {"type": "mrkdwn", "text": text}},)

    def get_message_payload(self):
        return {"channel": self.channel, "blocks": [self.NET_BLOCK, *self._get_facts()]}
