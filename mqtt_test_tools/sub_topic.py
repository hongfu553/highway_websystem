import paho.mqtt.client as mqtt

# server info
MQTT_BROKER = "hongfu553.myds.me"  # ip
MQTT_PORT = 1883  
MQTT_TOPIC = "tofu/road"  # topic


def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))
    client.subscribe(MQTT_TOPIC)

def on_message(client, userdata, msg):
    print("Received message: "+msg.payload.decode())

client = mqtt.Client()

client.on_connect = on_connect
client.on_message = on_message

client.connect(MQTT_BROKER, MQTT_PORT, 60)
client.loop_forever()
