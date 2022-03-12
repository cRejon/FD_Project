# -*- coding: utf-8 -*-
import paho.mqtt.client as pahoMQTT
import paho.mqtt.publish as publish
import json 
import time

inside_state = "disconnected"
soil_hum = 0  # percentage
min_soil_hum = 0 # percentage
irrig_time = 0  # seconds


def on_connect(client, userdata, flags, rc):
    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.
    client.subscribe("greenhouse1/state/inside")
    client.publish("greenhouse1/irrigation", '{"id": "irrigation","values": {"min_soil_hum": 0,"irrig_time": 0}}', retain= True)
    client.subscribe("greenhouse1/irrigation")


def read_message(message):
    global inside_state
    payload = str(message.payload).split("'")
    data = json.loads(payload[1])
    if message.topic == "greenhouse1/state/inside":
        if data["signal"] == "disconnected":
            inside_state = "disconnected"
            return "disconnected"
        else:
            inside_state="connected"
            return [data["values"]["soil_hum"]]
        
    else: # message comes from greenhouse1/irrigation
        return [data["values"]["min_soil_hum"], data["values"]["irrig_time"]]
     

def start_irrigation(client, userdata, message):
    global soil_hum, min_soil_hum, irrig_time, inside_state
    
    data = read_message(message)
    
    if data != "disconnected":
        if message.topic == "greenhouse1/state/inside": 
            soil_hum = data[0]  
        else:
            [min_soil_hum, irrig_time] = data
      
    if inside_state != "disconnected":
        if (soil_hum < min_soil_hum) & (irrig_time!= 0) :
            publish.single("greenhouse1/control/deposit", "activate_pump", qos=2, hostname="localhost", keepalive=1) # does not use client because it is slee
            time.sleep(irrig_time)
            client.publish("greenhouse1/control/deposit", "apagar_pump", qos=2)
            

client = pahoMQTT.Client(client_id="irrigation")
client.on_connect = on_connect
client.message_callback_add("greenhouse1/state/inside",start_irrigation)
client.message_callback_add("greenhouse1/irrigation",start_irrigation)
client.connect("localhost", 1883, 500) # keepalive=500
client.loop_forever()