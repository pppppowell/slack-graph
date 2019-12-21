from flask import Flask
from slackeventsapi import SlackEventAdapter
import subprocess
import requests
import os

ENV_VAR = os.environ["ENV_VAR"]
TOKEN=os.environ["TOKEN"]

app = Flask(__name__)

slack_events_adapter = SlackEventAdapter(ENV_VAR, "/slack/events",app)

@slack_events_adapter.on("message")
def hookSlackEvents(event_data):
    app.logger.debug(event_data)
    headers = {
        'X-USER-TOKEN': TOKEN,
        'Content-Length': '0',
    }
    event_data=event_data["event"]
    if "subtype" in event_data:
        if event_data["subtype"] == 'message_deleted':
            response = requests.put('https://pixe.la/v1/users/pppppowell/graphs/test-graph/decrement', headers=headers)
            print(response)
            print("decrement")
        elif event_data["subtype"] == 'message_changed':
            pass
    else:
        response = requests.put('https://pixe.la/v1/users/pppppowell/graphs/test-graph/increment', headers=headers)
        print(response)
        print(event_data["text"])
    

if __name__ == "__main__":
    app.run()
