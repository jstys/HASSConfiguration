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

assistant_room = None
mqtt_client = None

def on_connect(client, userdata, flags, rc):
    mqtt_client.subscribe('assistant/{}/tts'.format(assistant_room), qos=2)
    mqtt_client.subscribe('assistant/broadcast', qos=2)

def on_message(client, userdata, msg):
    message = msg.payload.strip().decode('utf-8')
    if msg.topic == BROADCAST_TOPIC:
        payload_split = message.split(":")
        message = payload_split[0].strip()
        source = payload_split[1].strip()
        if source == assistant_room:
            message = "Your message has been shared"

    pico_command = ['pico2wave', '-l', 'en-GB', '-w', 'tmp.wav', message]
    subprocess.call(pico_command)
    subprocess.call(['aplay', 'tmp.wav'])

def process_event(event, assistant):
    if event.type == EventType.ON_CONVERSATION_TURN_STARTED:
        subprocess.call(['aplay', 'hotword.wav'])

    if event.type == EventType.ON_RECOGNIZING_SPEECH_FINISHED:
        text = event.args.get('text')
        print("Raw: {}".format(text))

        intent, massaged_text = intent_parser.parse_intent(text)
        if intent is not None:
            assistant.stop_conversation()
            intent['raw'] = massaged_text
            intent['source'] = assistant_room
            mqtt_client.publish("assistant/{}/intent".format(assistant_room), payload=json.dumps(intent), qos=2)


def main():
    global assistant_room, mqtt_client

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
    parser.add_argument("broker_ip", type=str)
    parser.add_argument("broker_port", type=int)
    parser.add_argument("room_name", type=str)

    args = parser.parse_args()
    with open(args.credentials, 'r') as f:
        credentials = google.oauth2.credentials.Credentials(token=None,
                                                            **json.load(f))

    broker_ip = args.broker_ip
    broker_port = args.broker_port
    assistant_room = args.room_name
    mqtt_name = "_".join([assistant_room, "assistant"])
    mqtt_client = mqtt.Client(client_id=mqtt_name, protocol=mqtt.MQTTv31)

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
