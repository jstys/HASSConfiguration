from connections.mqtt_client_connection import MqttClientConnection

MQTT_PROTOCOL = "mqtt"

def create_connection(conncetion_protocol, connection_config, on_tts, on_broadcast, on_ask, on_broadcast_ask):
    if conncetion_protocol == MQTT_PROTOCOL:
        return create_mqtt_connection(connection_config, on_tts, on_broadcast, on_ask, on_broadcast_ask)
    else:
        return None

def create_mqtt_connection(connection_config, on_tts, on_broadcast, on_ask, on_broadcast_ask):
    connection = MqttClientConnection(connection_config, on_tts, on_broadcast, on_ask, on_broadcast_ask)
    if not connection.validate_config():
        return None
    else:
        return connection
