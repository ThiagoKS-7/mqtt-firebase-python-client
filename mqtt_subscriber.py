import os
import dotenv
import time
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

# As an admin, the app has access to read and write all data, regradless of Security Rules
ref = db.reference('nodemcu')
prevTemp = ref.get()["dht11"]["temperature"]["payload"]
prevHum = ref.get()["dht11"]["humidity"]["payload"]
TEMP_TOPIC="nodemcu/dht11/temperature"
HUM_TOPIC="nodemcu/dht11/humidity"


temperature_ref = ref.child("dht11/temperature")
humidity_ref = ref.child("dht11/humidity")


def on_message(client, userdata, message):        
    global prevHum
    global prevTemp 
    
    if "humidity" in message.topic:
        print(f'{message.topic}: Payload:{str(message.payload.decode("utf-8"))}% - QoS:{message.qos} - Retain:{message.retain}')
        if prevHum !=  f'{str(message.payload.decode("utf-8"))}%':
            humidity_ref.update({
                'payload': f'{str(message.payload.decode("utf-8"))}%',
                'qos': message.qos,
            })
            prevHum = ref.get()["dht11"]["humidity"]["payload"]
    else:
        print(f'{message.topic}: Payload:{str(message.payload.decode("utf-8"))}C - QoS:{message.qos} - Retain:{message.retain}')
        if prevTemp != f'{str(message.payload.decode("utf-8"))}C':
            temperature_ref.update({
                'payload': f'{str(message.payload.decode("utf-8"))}C',
                'qos': message.qos,
            })
            prevTemp = ref.get()["dht11"]["temperature"]["payload"]

# broker_address="192.168.1.184" 
print("[INFO] Starting Server...")
broker_address="mqtt.eclipseprojects.io" #use external broker
client = mqtt.Client("P1") #create new instance
client.on_message=on_message #attach function to callback
client.connect(broker_address) #connect to broker
client.loop_start()
print("[INFO] Broker connected")
client.subscribe(TEMP_TOPIC, qos=1)
client.subscribe(HUM_TOPIC, qos=1)
while True:
    time.sleep(10)