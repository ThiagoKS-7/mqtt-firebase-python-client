import os
import dotenv
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
import paho.mqtt.client as mqtt

dotenv.load_dotenv()
cred = credentials.Certificate(os.getenv('CRED_PATH'))

# Initialize the app with a service account, granting admin privileges
firebase_admin.initialize_app(cred,{
  'apiKey':  os.getenv('API_KEY'),
  'authDomain': os.getenv('AUTH_DOMAIN'),
  'databaseURL': os.getenv('DATABASE_URL'),
  'projectId':  os.getenv('PROJECT_ID'),
  'storageBucket':  os.getenv('STORAGE_BUCKET'),
  'messagingSenderId':  os.getenv('MESSAGING_SENDER_ID'),
 'appId':  os.getenv('APP_ID')
})

ref = db.reference('nodemcu')
temperature_ref = ref.child("dht11/temperature")
humidity_ref = ref.child("dht11/humidity")

# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))
    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.
    client.subscribe([("nodemcu/dht11/temperature", 1), ("nodemcu/dht11/humidity", 1)])

# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):
    print(msg.topic+": "+str(msg.payload.decode("utf-8"))+"- QoS: "+str(msg.qos))
    
    if "humidity" in msg.topic:
        humidity_ref.update({
            'payload': int(msg.payload.decode("utf-8")),
            'qos': msg.qos,
        })
    else:
        temperature_ref.update({
            'payload': int(msg.payload.decode("utf-8")),
            'qos': msg.qos,
        })

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

client.connect("mqtt.eclipseprojects.io", 1883, 60)

# Blocking call that processes network traffic, dispatches callbacks and
# handles reconnecting.
# Other loop*() functions are available that give a threaded interface and a
# manual interface.
client.loop_forever()