import paho.mqtt.client as mqtt

# server info
mqtt_broker = "hongfu553.myds.me"  # ip
mqtt_port = 1883  
mqtt_topic = "tofu/road"  # topic
#mqtt_user= "48losv5973"
#mqtt_password="3469fgjoxy"

def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))
    client.subscribe(mqtt_topic)

def on_message(client, userdata, msg):
    print("Received message: "+msg.payload.decode())

client = mqtt.Client()
#client.username_pw_set(username=mqtt_user, password=mqtt_password)

client.on_connect = on_connect
client.on_message = on_message

client.connect(mqtt_broker, mqtt_port, 60)
client.loop_forever()
