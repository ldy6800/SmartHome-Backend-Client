import paho.mqtt.client as mqtt
import pymysql as mysql
import csv
import threading
import bcrypt
import os
import sys

class Electricity(object):

	def __init__(self, current, volt, on):
		self.current = current
		self.volt = volt
		self.on = on

	def __init__(self, data):
		self.current = data[0]
		self.volt = data[1]
		self.on = data[2]

	def toCSV(self):
		return '{}, {}, {}'.format(self.current, self.volt, self.on)

def folderNameHash(userID):
	salt = bcrypt.gensalt()
	hashed = bcrypt.hashpw(userID.encode('utf-8'), salt)
	return hashed

def writeToCSV(folder, fileName, data):
	root = '/var/www/data/sensor'
	folder = root+'/{}'.format(folder)
	path = folder+'/{}'.format(fileName)
	print('root', root)
	print('folder', folder)
	print('path', path)
	if not os.path.isdir(folder):
		os.mkdir(folder)

	data = data.split(' ')
	data = Electricity(data)
	
	db = conn.cursor(mysql.cursors.DictCursor)
	db.execute('SELECT NOW()')
	date = db.fetchall()[0]['NOW()'].strftime('%Y-%m-%d %H:%M:%S')
	with open(path, mode='at', encoding='utf-8') as f:
		f.write(date + ', ' + data.toCSV() + '\n')
	os.chmod(path, 0o644)
	
def on_connect(client, userdata, flags, rc):
	print("Connected with result code " + str(rc))
	client.subscribe(topic)

def on_message_device(client, userdata, msg):
	print(msg.topic + " " + str(msg.payload))
	userID = msg.topic.split('/')[2] 
	deviceID = msg.topic.split('/')[3]
	db = conn.cursor(mysql.cursors.DictCursor)
	try:	
		sql = "SELECT folder FROM device where userID = %s and id = %s"
		#print(sql % (userID, deviceID))
		result = db.execute(sql, (userID, deviceID))
		data = db.fetchall()[0]['folder']
		if result > 0 :
			writeToCSV(data.split('/')[0], data.split('/')[1], msg.payload.decode('utf-8'))
		else :
			folder = userID + '/' + deviceID
			sql = "INSERT INTO device (id, userID, folder) SELECT %s, %s, %s FROM DUAL WHERE NOT EXISTS (SELECT userID FROM device WHERE id = %s AND userID = %s)"
			result = db.execute(sql, (deviceID, userID, folder, deviceID, userID))
			print('affected row: ', result)
	
	except Exception as e:
		print(e)	
	finally:	
		conn.commit()
		db.close()

def on_message_battery(client, userdata, msg):
	print(msg.topic + " " + str(msg.payload))
	userID = msg.topic.split('/')[3]
	db = conn.cursor(mysql.cursors.DictCursor)
	try:
		sql = "SELECT id FROM user where id = %s"
		result = db.execute(sql, (userID))
		#if result > 0:
		if result > 0:	
			writeToCSV(userID, sys.argv[1], msg.payload.decode('utf-8'))
	except Exception as e:
		print(e)
	finally:
		conn.commit()
		db.close()
client = mqtt.Client()
topic = sys.argv[1]
client.on_connect = on_connect
client.on_message = on_message_device
if topic == 'solar':
	topic = 'house/battery/solar/#'	
	client.on_message = on_message_battery
elif topic == 'external':
	topic = 'house/battery/external/#'
	client.on_message = on_message_battery
elif topic == 'solarGen':
	topic = 'house/solar/#'
	client.on_message = on_message_battery
elif topic == 'device':
	topic = 'house/device/#'
	client.on_message = on_message_device
	

client.connect("#########", 1883, 60)

conn = mysql.connect(host="##########", user="blank", password="blankblank", db="smartHome", charset="utf8")

try:
	client.loop_forever()
except KeyboardInterrupt:
	conn.close()
	print("EXIT")
