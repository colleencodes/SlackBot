import os
import time
import re
import random
from slackclient import SlackClient

#instantiate slack client
slack_client = SlackClient(os.environ.get('SLACK_BOT_TOKEN'))
#starterbot's user id in slack: value is assigned after the bot starts up
starterbot_id = None

#constants
RTM_READ_DELAY = 1 # 1 second elay between reading from RTM 
TRIGGER_COMMAND = "box"
MENTION_REGEX = "^<@(|[WU].+?)>(.*)"
# MENTION_R?EGEX = "^/box"
BOXING_MOVES = {
    1: 'jab',
    2: 'cross',
    3: 'left hook',
    4: 'right hook',
    5: 'left uppercut',
    6: 'right uppercut',
    7: 'slip forward',
    8: 'slip backward',
    9: 'roll under forward',
    10: 'roll under backward',
    11: 'duck',
    12: 'step back'
}

def parse_bot_commands(slack_events):
    """
    	Parses a list of events coming from Slack RTM API to find bot 
        commands.
        If a bot command is found, tihs function returns tuple of 
        command and channel.
        If its not found, then returns None, None.
    """
    for event in slack_events:
        print(event)
        if event["type"] == "message" and not "subtype" in event:
            user_id, message = parse_direct_mention(event["text"])
            if user_id == starterbot_id:
                return message, event["channel"]

    return None, None

def parse_direct_mention(message_text):
    """
        Finds a direct metion (mention at the beginning) in message text
        and returns the user ID which was mentioned. If there is not
        direct metnion, returns None
    """
    matches = re.search(MENTION_REGEX, message_text)

    #first group contains the username, the second group contains the
    #remaining message
    return (matches.group(1), matches.group(2).strip()) if matches else (None, None)

def  handle_command(command, channel):
    """
        Executes bot command if the command is known
    """
    #default response is help text for the user
    default_response = "Ducked because I don't understand! Try *{}*.".format(TRIGGER_COMMAND)

    boxing_move = None
    if command.startswith(TRIGGER_COMMAND):
        boxing_move = BOXING_MOVES[random.randint(1, len(BOXING_MOVES))] + '!'

    slack_client.api_call(
        "chat.postMessage",
        channel=channel,
        text=boxing_move or default_response
    )

if __name__ == "__main__":
    if slack_client.rtm_connect(with_team_state=False):
        print("Boxer Bot connected and running!")
        #read bot's user ID by calling web API method 'auth.test'
        starterbot_id = slack_client.api_call("auth.test")["user_id"]
        while True:
            command, channel = parse_bot_commands(slack_client.rtm_read())

            if command:
                handle_command(command, channel)
            time.sleep(RTM_READ_DELAY)

    else:
        print("Connection failed. Exception traceback printed above.")
