import paho.mqtt.client as mqtt

def on_connect(client, userdata, flags, rc):
    if rc == 0:
        client.connected_flag = True

def check_mqtt_status(broker_address, port):
    client = mqtt.Client("CheckClient")
    client.connected_flag = False
    client.on_connect = on_connect
    client.connect(broker_address, port, 60)
    client.loop_start()
    while not client.connected_flag:
        pass
    client.disconnect()
    return client.connected_flag
