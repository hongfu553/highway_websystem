#send message to mqtt broker
import ssl
import paho.mqtt.client as mqtt

broker='amd2.oracle.kenchou2006.eu.org'
port=1883
topic="tofu/road"

message ='hello'
#server info

client = mqtt.Client('send')

#client.tls_set(tls_version=ssl.PROTOCOL_TLS)
client.connect(broker,port)

client.publish(topic, message)

client.disconnect()
