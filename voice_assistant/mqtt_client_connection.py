import functools

import paho.mqtt.client as mqtt
from iconnection import IConnection

class MqttClientConnection(IConnection):
    
    BROADCAST_TTS_TOPIC = "assistant/broadcast/tts"
    BROADCAST_ASK_TOPIC = "assistant/broadcast/ask"
    
    def __init__(self, config):
        self._mqtt_client = None
        self._assistant_room = None
        self._tts_topic = None
        self._ask_topic = None
    
    def validate_config(self):
        pass
    
    def run_in_background(self):
        self._mqtt_client.loop_start()
        
    def on_connect(self, client, userdata, flags, rc):
        self._tts_topic = 'assistant/{}/tts'.format(self._assistant_room)
        self._ask_topic = 'assistant/{}/ask'.format(self._assistant_room)
        self._mqtt_client.subscribe(self._tts_topic, qos=2)
        self._mqtt_client.subscribe(self._ask_topic, qos=2)
        self._mqtt_client.subscribe(MqttClientConnection.BROADCAST_TTS_TOPIC, qos=2)
        self._mqtt_client.subscribe(MqttClientConnection.BROADCAST_ASK_TOPIC, qos=2)
        
    def on_message(self, client, userdata, msg):
        if msg.topic == self._tts_topic:
            pass
        elif msg.topic == self._ask_topic:
            pass
        elif msg.topic == MqttClientConnection.BROADCAST_TTS_TOPIC:
            pass
        elif msg.topic == MqttClientConnection.BROADCAST_ASK_TOPIC:
            pass