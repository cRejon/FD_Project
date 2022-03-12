# -*- coding: utf-8 -*-
import dash_bootstrap_components as dbc
import dash_html_components as html
import dash_core_components as dcc

from layout import get_gateway_connection

import json

IP_GETAWAY = open("./ip_getaway.txt", "r").read()

def serve_devices_layout():
    
    global_state = {}
    
    gateway_connected = get_gateway_connection()
    
    if gateway_connected == True:
        for node in ["inside","outside", "deposit", "climat"]:
            with open("./{}.txt".format(node), "r") as file:
                global_state[node] = json.loads(file.read())
           
            if global_state[node]["signal"] != "disconnected":
                global_state[node]["signal"] = str(global_state[node]["signal"])+" dBm"
            
    else:
        for node in ["inside","outside", "deposit", "climat"]:
            global_state[node] = {}
            global_state[node]["signal"] = "disconnected"
         
    layout = [
         html.Div(className="col-md-8 col-xl-12", children=[ 
                 dbc.Container(className="card theme-bg text-white f-12", children=[
                         dbc.Row(children=[
                                dbc.Col(width={"size": 4, "offset":4}, children=[
                                        dbc.Card(className="card theme-bg2 text-white f-12", children=[
                                                html.H4("Greenhouse_1", style={'padding':'5px','text-align':'center'}),
                                        ]),
                                ]),
                         ]), 
                         dbc.Row(children=[
                                dbc.Col(width={"size": 6}, children=[
                                         dbc.Card(className="card theme-bg2 text-white f-12", children=[
                                                 dbc.CardHeader("Gateway"),
                                                 dbc.CardBody([
                                                         dbc.Row([
                                                                 dbc.Col(width={"size": 10}, children=[
                                                                         html.H4("Raspberry Pi 3 model B", style={})
                                                                 ]),
                                                                 dbc.Col(width={"size": 2},align ="center", children=[
                                                                         dbc.CardLink("(+info)",
                                                                                      style={'color':'white','font-weight': '600'}, 
                                                                                      href="https://www.raspberrypi.org/products/raspberry-pi-3-model-b/",
                                                                                      target = "_blank"),
                                                                 ]),
                                                         ]),
                                                         html.Hr(className="my-2"),   
                                                         dbc.CardImg(src="/assets/images/raspberry_pi_3.webp", top=False),
                                                         dbc.Row(style={'padding-top':'25px'},children=[
                                                                 dbc.Col(width={"size": 6}, children=[        
                                                                         html.H5("Outgoing IP address:"),
                                                                 ]),
                                                                 dbc.Col(width={"size": 6}, children=[        
                                                                         html.H5(IP_GETAWAY, style={'text-align':'right'}),
                                                                 ]),
                                                         ]),
                                                         html.Hr(className="my-2"), 
                                                         dbc.Row(style={'padding-top':'10px'},children=[
                                                                 dbc.Col(width={"size": 10}, children=[        
                                                                         html.H5("Software installed"),
                                                                 ]),
                                                                 dbc.Col(width={"size": 2}, children=[        
                                                                         dbc.Button("Ver",id="gateway_software", size="sm", outline=True, color="light"),
                                                                 ]),
                                                         ]), 
                                                         html.Hr(className="my-2"),
                                                         dbc.Collapse(id="collapse_gateway_software", children=[
                                                                 dbc.Table(style={'font-weight': '600','color':'snow'},borderless =True,children=[
                                                                         html.Tr([html.Td("Raspbian"),  html.Td(style={'text-align':'center'},children=["10 (Buster)"])]),
                                                                         html.Tr([html.Td("Mosquitto"),  html.Td(style={'text-align':'center'},children=["1.6.9"])]),
                                                                         html.Tr([html.Td("Node-RED"),  html.Td(style={'text-align':'center'},children=["1.0.4"])]),
                                                                         html.Tr([html.Td("Python"),  html.Td(style={'text-align':'center'},children=["3.7.3"])]),
                                                                         html.Tr([html.Td(children=[dbc.Badge(style={'background':'#9A8FD1'},children=html.Div(className="feather icon-corner-down-right f-25")),"Paho MQTT"]),  html.Td(style={'text-align':'center'},children=["1.5.0"])]),                                                                 
                                                                         html.Tr([html.Td("Script irrigation"),  html.Td(style={'text-align':'center'},children=["1.0.0"])]),                                            
                                                                         html.Tr([html.Td("Script climat"),  html.Td(style={'text-align':'center'},children=["1.0.0"])]),
                                                                ]), 
                                                         ]),
                                                 ]),                                 
                
                                         ]),
                                ]),
                                dbc.Col(width={"size": 5}, children=[
                                         dbc.Card(className="card theme-bg2 text-white f-12", children=[
                                                 dbc.CardHeader("Nodes"),
                                                 dbc.CardBody([
                                                         dbc.Row([
                                                                 dbc.Col(width={"size": 9}, children=[
                                                                         html.H4("ESP8266 - NodeMCU", style={})
                                                                 ]),
                                                                 dbc.Col(width={"size": 3},align ="center", children=[
                                                                         dbc.CardLink("(+info)",
                                                                                      style={'color':'white','font-weight': '600'}, 
                                                                                      href="https://www.espressif.com/en/products/hardware/esp8266ex/overview",
                                                                                      target = "_blank"),
                                                                 ]),
                                                         ]),
                                                         html.Hr(className="my-2"),   
                                                         dbc.CardImg(src="/assets/images/nodeMCU.jpg", top=False),
                                                         dbc.Row(style={'padding-top':'25px'},children=[
                                                                 dbc.Col(width={"size": 6}, children=[        
                                                                         html.H5("Location"),
                                                                 ]),
                                                                 dbc.Col(width={"size": 6}, children=[        
                                                                         html.H5("Signal", style={'text-align':'center'}),
                                                                 ]),
                                                         ]),
                                                         html.Hr(className="my-2"), 
                                                         dbc.Row(style={'padding-top':'25px'},children=[
                                                                 dbc.Col(width={"size": 6},align ="center", children=[        
                                                                         html.H6("Inside"),                                                                        
                                                                 ]),
                                                                 dbc.Col(width={"size": 6}, children=[ 
                                                                         dbc.Row([
                                                                                 dbc.Col(width={"size": 9},align ="center", children=[
                                                                                         html.H6(global_state["inside"]["signal"], style={'text-align':'right'})
                                                                                 ]),
                                                                                 dbc.Col(width={"size": 1}, children=[
                                                                                         dbc.Button(html.Div(className="feather icon-info"), id="button_modal_inside", size="sm", outline=True, color="light"),
                                                                                 ]),
                                                                         ]),        
                                                                 ]),
                                                                 dbc.Modal(id="modal_inside",centered=True, children=[
                                                                         dbc.ModalHeader("Connected devices - @Inside"),
                                                                         dbc.ModalBody([
                                                                                 html.P("Temperature and humidity sensor DHT22"),
                                                                                 html.P("Capacitive soil moisture sensor"),
                                                                         ]),
                                                                         dbc.ModalFooter(
                                                                             dbc.Button("Close", id="close_modal_inside", className="ml-auto")
                                                                         ),
                                                                     ],
                                                                 ),
                                                         ]), 
                                                         dbc.Row(style={'padding-top':'25px'},children=[
                                                                 dbc.Col(width={"size": 6},align ="center", children=[  
                                                                         html.H6("Outside"),
                                                                 ]),
                                                                 dbc.Col(width={"size": 6}, children=[ 
                                                                         dbc.Row([
                                                                                 dbc.Col(width={"size": 9},align ="center", children=[
                                                                                         html.H6(global_state["outside"]["signal"], style={'text-align':'right'})
                                                                                 ]),
                                                                                 dbc.Col(width={"size": 1}, children=[
                                                                                         dbc.Button(html.Div(className="feather icon-info"), id="button_modal_outside", size="sm", outline=True, color="light"),
                                                                                 ]),
                                                                         ]),        
                                                                 ]),
                                                                 dbc.Modal(id="modal_outside",centered=True, children=[
                                                                         dbc.ModalHeader("Connected devices - @Outside"),
                                                                         dbc.ModalBody([
                                                                                 html.P("Temperature and humidity sensor"),
                                                                                 html.P("Door opening magnetic sensor"),
                                                                         ]),
                                                                         dbc.ModalFooter(
                                                                             dbc.Button("Close", id="close_modal_outside", className="ml-auto")
                                                                         ),
                                                                     ],
                                                                 ),
                                                         ]), 
                                                         dbc.Row(style={'padding-top':'25px'},children=[
                                                                 dbc.Col(width={"size": 6},align ="center", children=[        
                                                                         html.H6("Deposit"),
                                                                 ]),
                                                                 dbc.Col(width={"size": 6}, children=[ 
                                                                         dbc.Row([
                                                                                 dbc.Col(width={"size": 9},align ="center", children=[
                                                                                         html.H6(global_state["deposit"]["signal"], style={'text-align':'right'})
                                                                                 ]),
                                                                                 dbc.Col(width={"size": 1}, children=[
                                                                                         dbc.Button(html.Div(className="feather icon-info"), id="button_modal_deposit", size="sm", outline=True, color="light"),
                                                                                 ]),
                                                                         ]),        
                                                                 ]),
                                                                 dbc.Modal(id="modal_deposit",centered=True, children=[
                                                                         dbc.ModalHeader("Connected devices - @Deposit"),
                                                                         dbc.ModalBody([
                                                                                 html.P("Water temperature sensor"),
                                                                                 html.P("Irrigation pump actuator"),
                                                                         ]),
                                                                         dbc.ModalFooter(
                                                                             dbc.Button("Close", id="close_modal_deposit", className="ml-auto")
                                                                         ),
                                                                     ],
                                                                 ),
                                                         ]), 
                                                         dbc.Row(style={'padding-top':'25px'},children=[
                                                                 dbc.Col(width={"size": 6},align ="center", children=[        
                                                                         html.H6("Climat"),
                                                                 ]),
                                                                 dbc.Col(width={"size": 6}, children=[ 
                                                                         dbc.Row([
                                                                                 dbc.Col(width={"size": 9},align ="center", children=[
                                                                                         html.H6(global_state["climat"]["signal"], style={'text-align':'right'})
                                                                                 ]),
                                                                                 dbc.Col(width={"size": 1}, children=[
                                                                                         dbc.Button(html.Div(className="feather icon-info"), id="button_modal_climat", size="sm", outline=True, color="light"),
                                                                                 ]),
                                                                         ]),        
                                                                 ]),
                                                                 dbc.Modal(id="modal_climat",centered=True, children=[
                                                                         dbc.ModalHeader("Connected devices - @Climat"),
                                                                         dbc.ModalBody([
                                                                                 html.P("Ventilation actuator"),
                                                                                 html.P("Heating actuator"),
                                                                                 html.P("Refrigeration actuator"),
                                                                         ]),
                                                                         dbc.ModalFooter(
                                                                             dbc.Button("Close", id="close_modal_climat", className="ml-auto")
                                                                         ),
                                                                     ],
                                                                 ),
                                                         ]),
                                                 ]),                                 
                                         ]),
                                ]),
                        ]),
                ]),
        ]),                                                          
    ]
    
    return layout