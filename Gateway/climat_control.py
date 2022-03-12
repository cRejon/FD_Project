# -*- coding: utf-8 -*-
import paho.mqtt.client as pahoMQTT
import json

min_temp = 0.0
target_temp = 20.0
max_temp = 40.0
min_hum = 0
max_hum = 100

inside_state="disconnected"
outside_state="disconnected"
state= "shutdown" # possible values: shutdown, activate_ventilation, activate_heating or activate_refrigeration
humidity_ventilation = False

in_temp = 20.0
in_hum = 50 

out_temp = 20.0
out_hum = 50
door = 0


def on_connect(client, userdata, flags, rc):
    client.subscribe("greenhouse1/state/inside")
    client.subscribe("greenhouse1/state/outside")
    client.publish("greenhouse1/climatControl", '{"id": "climatControl","values": {"min_temp": 0.0,"target_temp": 20.0,"max_temp": 40.0,"min_hum": 0,"max_hum": 100}}', retain= True)
    client.subscribe("greenhouse1/climatControl") 
    client.publish("greenhouse1/control/climat", "shutdown", retain= True)
  

def read_message(message):
    global inside_state, outside_state
    mssg = str(message.payload).split("'")
    data =  json.loads(mssg[1])
    if message.topic == "greenhouse1/state/inside": 
        if data["signal"] == "disconnected":
            inside_state = data["signal"]
            return data["signal"]
        else:
            inside_state="connected"
            return [data["values"]["in_temp"], data["values"]["in_hum"]]

        
    elif message.topic == "greenhouse1/state/outside":
        if data["signal"] == "disconnected":
            outside_state = data["signal"] 
            return data["signal"] 
        else:
            outside_state="connected"
            return [data["values"]["out_temp"], data["values"]["out_hum"], data["values"]["door"]]
        
    else: # message from greenhouse1/climatControl 
        return [data["values"]["min_temp"], data["values"]["target_temp"], data["values"]["max_temp"], data["values"]["min_hum"], data["values"]["max_hum"]]


def get_next_state(client, userdata, message):
    global state, inside_state, outside_state, in_temp, in_hum, out_temp, out_hum, door, min_temp, target_temp, max_temp, min_hum, max_hum
    
    data = read_message(message)
    
    if data != "disconnected":
        if message.topic == "greenhouse1/state/inside": 
            [in_temp, in_hum] = data
            
        elif message.topic == "greenhouse1/state/outside":
            [out_temp, out_hum, door] = data
            
        else:
            [min_temp, target_temp, max_temp, min_hum, max_hum] = data
        
    if inside_state != "disconnected" and outside_state != "disconnected":
        func_dic = {
            "shutdown": system_off,
            "activate_ventilation": ventilating,
            "activate_heating": heating,
            "activate_refrigeration": refrigerating,
        }
        
        func = func_dic.get(state)
        next_state = func()
        if state != next_state:
            state = next_state
            client.publish("greenhouse1/control/climat", state, qos=2, retain= True)
        else:
            pass
    else:
        client.publish("greenhouse1/control/climat", "shutdown", qos=2, retain= True)
    

def system_off ():
    global in_temp, in_hum, out_temp, out_hum, min_temp, max_temp, max_hum, door, humidity_ventilation 
    # condition to turn on moisture ventilation
    if in_hum > max_hum and in_hum > out_hum + 10:
        humidity_ventilation = True
        return "activate_ventilation"
    # condition to turn on temperature ventilation
    elif (in_temp < min_temp and in_temp < out_temp -0.5) or (in_temp > max_temp and in_temp > out_temp +0.5):
        return "activate_ventilation"
    # conditions for turning on the heating
    elif (in_temp < min_temp) and (door == 0):
        return "activate_heating"
    # conditions for turning on refrigeration   
    elif (in_temp > max_temp) and (door == 0):
        return "activate_refrigeration"
    else:
        return "shutdown"
    
    
def ventilating():
    global in_temp, in_hum, out_temp, out_hum, min_temp, target_temp, max_temp, min_hum, max_hum, humidity_ventilation
    # conditions for shutdown ventilation
    if ((humidity_ventilation and (in_hum <= min_hum or in_hum <= out_hum +2 or (not min_temp +0.5 <= in_temp <= max_temp -0.5 and in_hum <= max_hum -10)))
        or (not humidity_ventilation and (out_temp -0.5 <= in_temp <= out_temp +0.5 or target_temp -0.5 <= in_temp <= target_temp +0.5))):
        humidity_ventilation = False
        return "shutdown"
    else:
        return "activate_ventilation"


def heating():
    global in_temp, target_temp, door 

    if (in_temp >= target_temp or door != 0):
        return "shutdown"
    else:
        return "activate_heating"
    
def refrigerating():
    global in_temp, target_temp, door 

    if (in_temp <= target_temp or door != 0):
        return "shutdown"
    else:
        return "activate_refrigeration"


client = pahoMQTT.Client(client_id="climatControl")
client.on_connect = on_connect
client.message_callback_add("greenhouse1/climatControl",get_next_state)
client.message_callback_add("greenhouse1/state/outside",get_next_state)
client.message_callback_add("greenhouse1/state/inside",get_next_state)
client.connect("localhost", 1883)
client.loop_forever()
