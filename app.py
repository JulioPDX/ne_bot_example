import os
import logging
from flask import Flask
from slack import WebClient
from slackeventsapi import SlackEventAdapter
from coinbot import CoinBot
from get_network import NetBot

# Initialize a Flask app to host the events adapter
app = Flask(__name__)

# Create an events adapter and register it to an endpoint in the slack app for event ingestion.
slack_events_adapter = SlackEventAdapter(
    os.environ.get("SLACK_EVENTS_TOKEN"), "/slack/events", app
)

# Initialize a Web API client
slack_web_client = WebClient(token=os.environ.get("SLACK_TOKEN"))

# Define bot ID so it will not respond to itself
BOT_ID = slack_web_client.api_call("auth.test")["user_id"]


def flip_coin(channel):
    """
    Craft the CoinBot, flip the coin and send the message to the channel
    """
    # Create a new CoinBot
    coin_bot = CoinBot(channel)

    # Get the onboarding message payload
    my_message = coin_bot.get_message_payload()

    # Post the onboarding message in Slack
    slack_web_client.chat_postMessage(**my_message)


def send_me_help(channel, device_name):
    """
    run send_help method
    """
    net_bot = NetBot(channel, device_name)
    file_output = net_bot.send_help()
    slack_web_client.files_upload(**file_output)


def get_network_info(channel, device_name):
    """
    run the get_message_payload and get_file_upload method
    """
    net_bot = NetBot(channel, device_name)
    my_message = net_bot.get_message_payload()
    file_output = net_bot.get_file_payload()
    slack_web_client.chat_postMessage(**my_message)
    slack_web_client.files_upload(**file_output)


# When a 'message' event is detected by the events adapter, forward that payload
# to this function.
@slack_events_adapter.on("message")
def message(payload):
    """
    Parse the message event, and if the activation string is in the text,
    simulate something and send result
    """

    # Get various portions of message
    event = payload.get("event", {})
    text = event.get("text")
    user_id = event.get("user")
    timestamp = event.get("ts")
    channel_id = event.get("channel")

    # Making sure the bot doesnt respond to itself
    if BOT_ID != user_id:
        # Check and see if the activation phrase was in the text of the message.
        # If so, execute the code to flip a coin.
        if "hey netbot flip coin" in text.lower():
            # Execute the flip_coin function and send the results of
            # flipping a coin to the channel
            return flip_coin(channel_id)

        if "netbot get network interfaces" in text.lower():
            full_text = text.split()
            device = full_text[-1]
            my_device = device.replace("device=", "")
            slack_web_client.reactions_add(
                channel=channel_id, name="robot_face", timestamp=timestamp
            )
            slack_web_client.reactions_add(
                channel=channel_id, name="rocket", timestamp=timestamp
            )
            return get_network_info(channel_id, device_name=my_device)

        if "netbot help" in text.lower():
            slack_web_client.reactions_add(
                channel=channel_id, name="sos", timestamp=timestamp
            )
            slack_web_client.reactions_add(
                channel=channel_id, name="interrobang", timestamp=timestamp
            )
            return send_me_help(channel_id, device_name="")


if __name__ == "__main__":
    # Create the logging object
    logger = logging.getLogger()

    # Set the log level to DEBUG. This will increase verbosity of logging messages
    logger.setLevel(logging.DEBUG)

    # Add the StreamHandler as a logging handler
    logger.addHandler(logging.StreamHandler())

    # Run your app on your externally facing IP address on port 3000 instead of
    # running it on localhost, which is traditional for development.
    app.run(host="0.0.0.0", port=3000)
