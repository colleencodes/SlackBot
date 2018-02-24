import os
import time
import re
from slackclient import SlackClient

#instantiate slack client
slack_client = SlackClient(os.environ.get('SLACK_BOT_TOKEN'))
#starterbot's user id in slack: value is assigned after the bot starts up
starterbot_id = None

#constants
RTM_READ_DELAY = 1 # 1 second elay between reading from RTM 
EXAMPLE_COMMAND = "do"
MENTION_REGEX = "^@(|[WU].+?)>(.*)"

def parse_bot_commands(slack_events):
    """
    	Parses a list of events coming from Slack RTM API to find bot 
        commands.
        If a bot command is found, tihs function returns tuple of 
        command and channel.
        If its not found, then returns None, None.
    """
    for event in slack_events:
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

    #first group contains teh username, the second group contains the
    #remaining message
    return (matches.group(1), matches.group(2).strip()) if matches else (None, None)

def  handle_command(command, channel):
    """
        Executes bot command if the command is known
    """
    #default response is help text for the user
    default_response = "Not sure what you mean. Try *{}*.".format(EXAMPLE_COMMAND)

    #Finds and executes the given command, fillingin the response
    response = None

    #where to implement bot's abilities
    if command.startswith(EXAMPLE_COMMAND):
        response = "Write me some code!"

    #Sends response back to channel
    slack_client.api_call(
        "chat.postMessage",
        channel=channel,
        text=response or default_response
    )

if __name__ == "__main__":
    print(SlackClient(os.environ.get('SLACK_BOT_TOKEN')))
    print(' ')
    if slack_client.rtm_connect(with_team_state=False):
        print("Starter Bot connected and running!")
        #read bot's user ID by calling web API method 'auth.test'
        starterbot_id = slack_client.api_call("auth.test")["user_id"]
        while True:
            command, channel = parse_bot_commands(slack_client.rtm_read())

            if command:
                handle_command(command, channel)
            time.sleep(RTM_READ_DELAY)

    else:
        print("Connection failed. Exception traceback printed above.")


