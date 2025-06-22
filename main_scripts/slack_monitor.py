from slack_bolt import App
from slack_bolt.adapter.socket_mode import SocketModeHandler
import logging
import os
from reactions.incidentio_reaction import msg_alert_to_AppSupport
from reactions.slack_reaction import post_msg_to_channel
from dotenv import dotenv, dotenv_values

#Start logging
logging.basicConfig(level=logging.INFO)

#mappings to get target msg
channel_citi_mappping={
    'C06RC718WHX': (['threshold crossed', 'step-functions-failed', 'critical', 'not mapped on yieldcurvelookup table','[mds checker] error'], 
                    '#logs-prod', 'C082JQ9LXDK'),
    'C06QZHAHH4J': (['[mds checker] error'], '#logs-staging','C082JQ9LXDK'),
    'C07NGN4M2LF': (['error', 'failed'], '#logs-risk','C082JQ9LXDK'),
    'C08DJTQ578X': (['failed'],'#logs-pnl-runs-prod','C082JQ9LXDK')
}

channel_tag_mapping={
    's07v5f7p5nz': ('C082JQ9LXDK', '@middle-office'), #tag mo (update to correct value later)
    's07ajadld17': ('C082JQ9LXDK', '@app-support')
}

#get credential to connect with slack bot
load_dotenv()
SLACK_BOT_TOKEN = os.getenv('SLACK_BOT_TOKEN')
SLACK_APP_TOKEN = os.getenv('SLACK_APP_TOKEN')

app = App(token=SLACK_BOT_TOKEN)

#Function to generate slack msg link to main thread of sub thread
def generate_url(event, channel):
    is_subthread=event.get("thread_ts", 0)
    this_thread_ts = event.get("ts")
    if is_subthread != 0:
        link=f'https://arrowpointfund.slack.com/archives/{channel}/p{this_thread_ts}?thread_ts={is_subthread}&cid={channel}'
    else:
        link = f'https://arrowpointfund.slack.com/archives/{channel}/p{this_thread_ts}'
    return link

@app.event("message") #monitor to all message 
def message(body, logger, client):
    event = body.get("event", {})
    text = str(event.get("text")).lower()
    channel = event.get("channel")
    link = generate_url(event, channel)
    if channel in channel_citi_mappping.keys() and any(word in text for word in channel_citi_mappping[channel][0]):
        logger.info(body)
        keywords, channel_name, channel_to_send = channel_citi_mappping[channel]
        msg_alert_to_AppSupport(f'Alert from {channel_name}!\n{link}')
    if any(slack_id in text for slack_id in channel_tag_mapping.keys()):
        logger.info(body)
        tagged_id = None
        for id in channel_tag_mapping.keys():
            if id in text:
                tagged_id = id
        post_msg_to_channel(channel_tag_mapping[tagged_id][0], f'{channel_tag_mapping[tagged_id][1]}! {link}')

if __name__ == "__main__":
    handler = SocketModeHandler(app, SLACK_APP_TOKEN)
    handler.start()