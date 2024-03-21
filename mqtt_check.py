import paho.mqtt.client as mqtt

def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("Connected to MQTT Broker!")
        client.connected_flag = True
    else:
        print("Failed to connect, return code %d\n", rc)

def check_mqtt_status(broker_address, port):
    client = mqtt.Client("CheckClient")
    client.connected_flag = False
    client.on_connect = on_connect
    print("=================================")
    print("by mqtt_check.py")
    print("Connecting to MQTT Broker...")
    print("=================================")
    client.connect(broker_address, port, 60)
    client.loop_start()
    while not client.connected_flag:
        pass
    client.disconnect()
    return client.connected_flag
