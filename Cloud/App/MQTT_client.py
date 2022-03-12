# -*- coding: utf-8 -*-
import paho.mqtt.client as pahoMQTT
import sys

IP_GETAWAY = str(sys.argv[1])

def on_connect(client, userdata, flags, rc):
    open("./text_files/ip_getaway.txt", "w").write(IP_GETAWAY)
        
    for node in ["inside", "outside", "deposit", "climat"]:
        client.subscribe("greenhouse1/estate/{}".format(node))


def save(client, userdata, message):
    
    msg = str(message.payload).split("'")[1]
    node = msg.topic.split("/")[2]
    with open("./text_files/{}.txt".format(node), "w") as text_file:
        text_file.write("{}".format(msg))
        

client = pahoMQTT.Client(client_id="app")
client.on_connect = on_connect
for node in ["inside", "outside", "deposit", "climat"]:
    client.message_callback_add("greenhouse1/estate/{}".format(node), save)

client.connect(str(IP_GETAWAY), 1883, keepalive=500) 

client.loop_forever()