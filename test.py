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
		client.publish("house/battery/solar/smartHome/5", "1, 2, 3, 4")
		time.sleep(3)
except KeyboardInterrupt:
	print("EXIT")
