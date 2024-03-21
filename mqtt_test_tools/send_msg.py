import paho.mqtt.client as mqtt

#server info
client = mqtt.Client()
client.connect("hongfu553.myds.me", 1883)

client.publish("tofu/road", "hello world by KenChou")

client.disconnect()
