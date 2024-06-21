import paho.mqtt.client as mqtt
import os

# MQTT 配置
mqtt_broker = os.getenv('broker')
mqtt_port = int(os.getenv('port'))
mqtt_username = os.getenv('username')
mqtt_password = os.getenv('password')

client = mqtt.Client('web')

if mqtt_username and mqtt_password:
    client.username_pw_set(mqtt_username, mqtt_password)

client.connect(mqtt_broker, mqtt_port)

def connect_mqtt():
    try:
        client.connect(mqtt_broker, mqtt_port)
    except Exception as e:
        print(f"Failed to connect to MQTT broker: {e}")
# 定义一个用于发布消息的函数
def publish_message(topic, message):
    client.publish(topic, message)