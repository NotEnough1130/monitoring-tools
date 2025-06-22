import logging
from slack_sdk import WebClient
from config.call_env_variable import get_env

#Start logging
logging.basicConfig(level=logging.INFO)

# Set up Slack credentials
SLACK_BOT_TOKEN = get_env('SLACK_BOT_TOKEN')
client = WebClient(token=SLACK_BOT_TOKEN)

# Function to add a reaction / emoji to a thread
def reaction_to_msg(channel, ts, sticker_name='white_check_mark'):
    try:
        client.reactions_add(
            channel=channel,
            name=sticker_name,
            timestamp=ts
        )
        logging.info('Reaction Completed!')
    except Exception as e:
        logging.error(f"Failed to add reaction: {e}")


# Function to capture message information from a Slack channel
def capture_msg_info(channel, start_time, end_time):
    messages = []
    has_more = True
    next_cursor = None
    while has_more:
        try:
            response = client.conversations_history(
                channel=channel,
                oldest=start_time,
                latest=end_time,
                inclusive=True,
                limit=1000,
                cursor=next_cursor
            )

            messages.extend(response["messages"])
            # Correctly update next_cursor and has_more
            next_cursor = response.get("response_metadata", {}).get("next_cursor")
            has_more = bool(next_cursor)
        except Exception as e:
            logging.error(f"Slack API error: {e}")
            break
    return messages

# Function to capture sub thread's info
def capture_reply_info(channel_id, thread_ts):
    messages = []
    has_more = True
    next_cursor = None
    response = client.conversations_replies(
        channel=channel_id,
        ts=thread_ts
    )
    messages.extend(response["messages"])
    next_cursor = response.get("response_metadata", {}).get("next_cursor")
    has_more = bool(next_cursor)
    return messages

# Function to post msg on thread
def post_msg_to_channel(channel, text):
    try:
        response = client.chat_postMessage(
            channel=channel,
            text=text
        )
        logging.info(f"Message posted successfully: {response['ts']}")
    except Exception as e:
        logging.error(f"Failed to post message: {e}")
