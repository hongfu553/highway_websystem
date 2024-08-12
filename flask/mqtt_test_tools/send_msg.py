#send message to mqtt broker
import ssl
import paho.mqtt.client as mqtt

broker='highway.us.to'
port=1883
topic="tofu/road"
username='hongfu553'
password='F132369445'

message ='hello'
#server info

client = mqtt.Client('send')
client.username_pw_set(username, password)
#client.tls_set(cert_reqs=ssl.CERT_NONE)
client.connect(broker,port)

client.publish(topic, message)

client.disconnect()
