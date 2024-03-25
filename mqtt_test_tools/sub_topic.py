#sub message on mqtt broker
import paho.mqtt.client as mqtt
import ssl

# server info
mqtt_broker = "amd2.oracle.kenchou2006.eu.org"  # ip
mqtt_port = 1883  
mqtt_topic = "tofu/road"  # topic

def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))
    client.subscribe(mqtt_topic)

def on_message(client, userdata, msg):
    print("Received message: "+msg.payload.decode())

client = mqtt.Client('sub')
#client.tls_set(tls_version=ssl.PROTOCOL_TLS)
client.on_connect = on_connect
client.on_message = on_message

client.connect(mqtt_broker, mqtt_port, 60)
client.loop_forever()
