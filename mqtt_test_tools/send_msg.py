import paho.mqtt.client as mqtt

broker='hongfu553.myds.me'
port=1883
topic='tofu/road'
#user='48losv5973'
#passwd='3469fgjoxy'
#server info
client = mqtt.Client()
#client.username_pw_set(username=user,password=passwd)
client.connect(broker,port)

client.publish("topic", "hello world by tofu")

client.disconnect()
