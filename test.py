import paho.mqtt.client as mqtt
import time
broker = '203.250.148.23'
port = 1883

def on_publish(client, userdata, result):
	print("pub")
	pass

client = mqtt.Client()
client.on_publish = on_publish

client.connect(broker, port)

try:
	while True:
		client.publish("house/battery/solar/smartHome", "1.0 13 1")
		client.publish("house/battery/external/smartHome", "1.0 13 1")
		client.publish("house/device/smartHome/1", "1.0 13 1")		
		client.publish("house/solar/smartHome", "1.0 13 1")
		time.sleep(1)
except KeyboardInterrupt:
	print("EXIT")
