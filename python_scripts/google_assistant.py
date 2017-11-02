#!/usr/bin/env python

# Copyright (C) 2017 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.


from __future__ import print_function

import argparse
import os.path
import json
import subprocess

import paho.mqtt.client as mqtt
import google.oauth2.credentials

from google.assistant.library import Assistant
from google.assistant.library.event import EventType
from google.assistant.library.file_helpers import existing_file

import intent_parser

BROADCAST_TOPIC = "assistant/broadcast"

assistant_room = "living_room" #TODO: parameterize this
mqtt_name = "_".join([assistant_room, "assistant"]) #TODO: parameterize this
mqtt_client = mqtt.Client(client_id=mqtt_name, protocol=mqtt.MQTTv31)

def on_connect(client, userdata, flags, rc):
    mqtt_client.subscribe('assistant/{}/tts'.format(assistant_room), qos=2)
    mqtt_client.subscribe('assistant/broadcast', qos=2)
    print("MQTT Connected")

def on_message(client, userdata, msg):
    print('TTS Output: {}'.format(msg.payload))
    message = msg.payload
    if msg.topic == BROADCAST_TOPIC:
        payload_split = msg.payload.split(":")
        message = payload_split[0]
        source = payload_split[1]
        if source == assistant_room:
            return

    subprocess.call(['pico2wave', '-w', 'tmp.wav', message])
    subprocess.call(['aplay', 'tmp.wav'])

def process_event(event, assistant):
    if event.type == EventType.ON_CONVERSATION_TURN_STARTED:
        print("Received Hotword")

    if event.type == EventType.ON_RECOGNIZING_SPEECH_FINISHED:
        text = event.args.get('text')
        print("Raw: {}".format(text))

        intent = intent_parser.parse_intent(text)
        if intent is not None:
            assistant.stop_conversation()
            intent['raw'] = text
            print(json.dumps(intent, indent=4))
            mqtt_client.publish("assistant/{}/intent".format(assistant_room), payload=json.dumps(intent), qos=2)
        else:
            print("Intent is None, leave it to google")


def main():
    parser = argparse.ArgumentParser(
        formatter_class=argparse.RawTextHelpFormatter)
    parser.add_argument('--credentials', type=existing_file,
                        metavar='OAUTH2_CREDENTIALS_FILE',
                        default=os.path.join(
                            os.path.expanduser('~/.config'),
                            'google-oauthlib-tool',
                            'credentials.json'
                        ),
                        help='Path to store and read OAuth2 credentials')
    args = parser.parse_args()
    with open(args.credentials, 'r') as f:
        credentials = google.oauth2.credentials.Credentials(token=None,
                                                            **json.load(f))


    # TODO: add more arguments
    broker_ip = "10.0.0.6"
    broker_port = 1883

    mqtt_client.on_connect = on_connect
    mqtt_client.on_message = on_message
    mqtt_client.username_pw_set(mqtt_name)
    mqtt_client.connect(broker_ip, broker_port)
    mqtt_client.loop_start()

    with Assistant(credentials) as assistant:
        for event in assistant.start():
            process_event(event, assistant)


if __name__ == '__main__':
    main()
