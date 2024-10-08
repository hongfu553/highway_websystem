#sub message on mqtt broker
import paho.mqtt.client as mqtt
import ssl

mqtt_broker = "highway.us.to"  # ip
mqtt_port = 1883
mqtt_topic = "tofu/road"  # topic
username='hongfu553'
password='F132369445'
def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))
    client.subscribe(mqtt_topic)

def on_message(client, userdata, msg):
    print("Received message: "+msg.payload.decode())

client = mqtt.Client('sub')
client.username_pw_set(username, password)
#client.tls_set(cert_reqs=ssl.CERT_NONE)
client.on_connect = on_connect
client.on_message = on_message

client.connect(mqtt_broker, mqtt_port, 60)
client.loop_forever()
