from connections.mqtt_client_connection import MqttClientConnection

MQTT_PROTOCOL = "mqtt"

def create_connection(conncetion_protocol, connection_config, assistant_room, on_tts, on_broadcast, on_ask, on_broadcast_ask, **user_callbacks):
    if conncetion_protocol == MQTT_PROTOCOL:
        return create_mqtt_connection(connection_config, assistant_room, on_tts, on_broadcast, on_ask, on_broadcast_ask, **user_callbacks)
    else:
        return None

def create_mqtt_connection(connection_config, assistant_room, on_tts, on_broadcast, on_ask, on_broadcast_ask, **user_callbacks):
    connection = MqttClientConnection(connection_config, assistant_room, on_tts, on_broadcast, on_ask, on_broadcast_ask, user_callbacks)
    if not connection.validate_config():
        return None
    else:
        return connection
