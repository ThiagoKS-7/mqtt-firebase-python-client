import paho.mqtt.client as mqtt #import the client1
import time

def on_message(client, userdata, message):
        
    if "humidity" in message.topic:
        print(f'{message.topic}: Payload:{str(message.payload.decode("utf-8"))}% - QoS:{message.qos} - Retain:{message.retain}')
    else:
        print(f'{message.topic}: Payload:{str(message.payload.decode("utf-8"))}C - QoS:{message.qos} - Retain:{message.retain}')

# broker_address="192.168.1.184" 
broker_address="mqtt.eclipseprojects.io" #use external broker
client = mqtt.Client("P1") #create new instance
client.on_message=on_message #attach function to callback
client.connect(broker_address) #connect to broker
client.loop_start() #start the loop
client.subscribe("nodemcu/dht11/temperature", qos=1)
client.subscribe("nodemcu/dht11/humidity", qos=1)

while True:
    time.sleep(4) # wait