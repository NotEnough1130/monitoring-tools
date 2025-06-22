import requests
import logging
from config.call_env_variable import get_env

#Start logging
logging.basicConfig(level=logging.INFO)

# Set up Incident.io credentials
incidentio_endpoint = get_env('iio_url')
incidentio_api_key = get_env('iio_token')

# Function to send alert to on-call App Support member
def msg_alert_to_AppSupport(msg_title):
    headers = {
        "Authorization": f"Bearer {incidentio_api_key}"
    }
    data = {
        "title": msg_title,
        "status": "firing",
    }
    try:
        response = requests.post(incidentio_endpoint, headers=headers, json=data) # Send alert to Incident.io
        if response.status_code == 202:
            logging.info("Alert sent successfully!")
        else:
            logging.error(f"Failed to send alert: {response.text}")
    except Exception as e:
        logging.error(f"Error sending alert: {e}")