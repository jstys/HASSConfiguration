import functools

import paho.mqtt.client as mqtt
from connections.iconnection import IConnection

class MqttClientConnection(IConnection):
    
    BROADCAST_TTS_TOPIC = "assistant/broadcast/tts"
    BROADCAST_ASK_TOPIC = "assistant/broadcast/ask"
    SNIPS_INTENT_TOPIC = "hermes/intent/+"
    MQTT_V_3_1 = "3.1"
    MQTT_V_3_1_1 = "3.1.1"
    
    def __init__(self, config, assistant_room, on_tts, on_broadcast, on_ask, on_broadcast_ask, **user_callbacks):
        super().__init__(config, assistant_room, on_tts, on_broadcast, on_ask, on_broadcast_ask)
        self._mqtt_client = None
        self._client_id = None
        self._broker_host = None
        self._broker_port = None
        self._tts_topic = None
        self._ask_topic = None
        self._username = None
        self._password = None
        self._mqtt_version = None
        for topic in user_callbacks.iteritems():
            self._user_callbacks[topic] = user_callbacks[topic]
        
    
    def validate_config(self):
        try:
            self._broker_host = self._config['broker_host']
        except:
            print("Missing broker_host setting for mqtt")
            return False

        try:
            self._broker_port = self._config['broker_port']
        except:
            print("Missing broker_port from mqtt config")
            return False

        try:
            self._client_id = self._config['client_id']
        except:
            print("Missing client_id from mqtt config")
            return False

        try:
            self._mqtt_version = self._config['mqtt_version']
            if self._mqtt_version == MqttClientConnection.MQTT_V_3_1:
                self._mqtt_version = mqtt.MQTTv31
            else:
                self._mqtt_version = mqtt.MQTTv311
        except:
            print("Missing mqtt_version from mqtt config")
            return False

        self._username = self._config.get("username")
        self._password = self._config.get("password")
        return True
    
    def run_in_background(self):
        self._mqtt_client = mqtt.Client(client_id=self._client_id, protocol=self._mqtt_version)
        self._mqtt_client.on_connect = self.on_connect
        self._mqtt_client.on_message = self.on_message
        if self._username:
            self._mqtt_client.username_pw_set(self._username, password=self._password)
        self._mqtt_client.connect(self._broker_host, self._broker_port)
        self._mqtt_client.loop_start()
        
    def on_connect(self, client, userdata, flags, rc):
        self._tts_topic = 'assistant/{}/tts'.format(self._assistant_room)
        self._ask_topic = 'assistant/{}/ask'.format(self._assistant_room)
        self._mqtt_client.subscribe(self._tts_topic, qos=2)
        self._mqtt_client.subscribe(self._ask_topic, qos=2)
        self._mqtt_client.subscribe(MqttClientConnection.BROADCAST_TTS_TOPIC, qos=2)
        self._mqtt_client.subscribe(MqttClientConnection.BROADCAST_ASK_TOPIC, qos=2)
        self._mqtt_client.subscribe(MqttClientConnection.SNIPS_INTENT_TOPIC, qos=2)
        
    def on_message(self, client, userdata, msg):
        if msg.topic == self._tts_topic:
            self._on_tts_message(msg.payload.decode('utf-8'))
        elif msg.topic == self._ask_topic:
            # TODO: add support for follow up intents
            self._on_ask_message(msg.payload.decode('utf-8'))
        elif msg.topic == MqttClientConnection.BROADCAST_TTS_TOPIC:
            msg_split = msg.payload.decode('utf-8').split(":")
            message = msg_split[0]
            source = msg_split[1]
            self._on_broadcast_message(message, source)
        elif msg.topic == MqttClientConnection.BROADCAST_ASK_TOPIC:
            msg_split = msg.payload.decode('utf-8').split(":")
            message = msg_split[0]
            source = msg_split[1]
            self._on_broadcast_ask_message(message, source)
        elif msg.topic in self._user_callbacks:
            self._user_callbacks[msg.topic](msg)
            

    def send_message(self, message, source=None):
        self._mqtt_client.publish("assistant/{}/intent".format(source), message, qos=2)
