import random


class CoinBot:
    """
    Main stuff to format messages
    """

    COIN_BLOCK = {
        "type": "section",
        "text": {"type": "mrkdwn", "text": ("Sure! Flipping a coin....\n\n")},
    }

    def __init__(self, channel):
        self.channel = channel

    def _flip_coin(self):
        rand_int = random.randint(0, 1)
        if rand_int == 0:
            results = "Heads"
        else:
            results = "Tails"

        text = f"The result is {results}"

        return ({"type": "section", "text": {"type": "mrkdwn", "text": text}},)

    def get_message_payload(self):
        return {
            "channel": self.channel,
            "blocks": [self.COIN_BLOCK, *self._flip_coin()],
        }
