# -*- coding: utf-8 -*-
import dash_bootstrap_components as dbc
import dash_html_components as html
import dash_core_components as dcc

from layout import get_gateway_connection

          
def get_wifi_icon(signal):
    if signal == "disconnected":
        return "feather icon-wifi-off f-20"
    else:
        return "feather icon-wifi f-20"
    

def serve_facilities_layout():
    
    layout = []
    
    gateway_connected = get_gateway_connection()
    
    if gateway_connected == True:
        
        layout = [  
            dcc.Interval(id='interval_facilities', interval=1*3000,n_intervals=0),
            dbc.Card(className="card rides-card",style={'background':'#303435'}, children=[
                    dbc.CardBody([
                            dbc.Card(
                                    dbc.CardBody(
                                            html.Div(style={'background-image':'url(/assets/images/maqueta2.jpg)','background-repeat': 'no-repeat','height':'590px','width':'780px'}, children=[ 
                                                    dbc.Row([
                                                            dbc.Col(width={"size": 4, "offset":0}, children =[
                                                                 dbc.Card(className="card theme-bg text-white f-12", children=[
                                                                         html.H3("Greenhouse_1", style={'text-align':'center'}),
                                                                 ]),
                                                            ]),
                                                    ]),        
                                                    dbc.Row([
                                                            dbc.Col(width={"size": 3, "offset":9}, children =[
                                                                    dbc.Button(id="button_popover_outside", className="theme-bg2",children=[
                                                                            dbc.Badge(className="theme-bg" ,children=[
                                                                                    html.I(id="img_button_outside")
                                                                            ]),
                                                                            "   Outside",
                                                                    ]),
                                                                    dbc.Popover(children=[
                                                                            dbc.PopoverBody(className="theme-bg2 text-white",children=[
                                                                                     dbc.Card(className="card theme-bg text-white f-12", children=[                                                                            
                                                                                             dbc.CardBody([
                                                                                                     html.H5("Temperature", className="card-title"),
                                                                                                     dbc.Row([
                                                                                                            dbc.Col(
                                                                                                                   html.I(className="fas fa-thermometer-half f-40", style={'color':'purple'}),
                                                                                                                   width={"size": 3, "offset": 1},
                                                                                                            ),        
                                                                                                            dbc.Col(
                                                                                                                   html.H3(id="out_temp",style={'color':'purple', "textAling":"center"}),
                                                                                                                   width={ "offset": 2},
                                                                                                            ),                                                      
                                                                                                    ]),
                                                                                                     html.Hr(className="my-2"), 
                                                                                                     html.H5("Humidity", className="card-title"),
                                                                                                     dbc.Row([
                                                                                                            dbc.Col(
                                                                                                                   html.I(className="feather icon-upload-cloud f-40", style={'color':'purple'}),
                                                                                                                   width={"size": 3, "offset": 1},
                                                                                                            ),                                                              
                                                                                                            dbc.Col(
                                                                                                                   html.H3(id="out_hum",style={'color':'purple', "textAling":"center"}),
                                                                                                                   width={"size": "auto", "offset": 1},
                                                                                                            ), 
                                                                                                    ]),
                                                                                                     html.Hr(className="my-2"), 
                                                                                                     html.H5("Door", className="card-title"),
                                                                                                     dbc.Row(id="door"),
                                                                                             ]),
                                                                                     ]),
                                                                            ]),                
                                                                        ],
                                                                        id="popover_outside",
                                                                        is_open=False,
                                                                        target="button_popover_outside",
                                                                        placement="right",
                                                                    ),
                                                            ]),
                                                    ]),
                                                    dbc.Row([
                                                            dbc.Col(width={"size": 4, "offset":0}, children =[
                                                                html.H1(".", style={'color':'white'}),
                                                            ]),
                                                    ]),
                                                    dbc.Row([
                                                            dbc.Col(width={"size": 4, "offset":0}, children =[
                                                                html.H1(".", style={'color':'white'}),
                                                            ]),
                                                    ]),        
                                                    dbc.Row([
                                                            dbc.Col(width={"size": 3, "offset":4}, children =[
                                                                    dbc.Button(id="button_popover_climat", className="theme-bg2",children=[
                                                                            dbc.Badge(className="theme-bg" ,children=[
                                                                                    html.I(id="img_button_climat")
                                                                            ]),
                                                                            "   Climat",
                                                                    ]),
                                                                    dbc.Popover([
                                                                            dbc.PopoverBody(className="theme-bg2 text-white", children=[
                                                                                     dbc.Card(className="card theme-bg text-white f-12", children=[
                                                                                             #dbc.CardHeader("@invernadero1/estado/deposit"),
                                                                                             dbc.CardBody(children=[ 
                                                                                                     html.H5("Ventilation", className="card-title"),
                                                                                                     dbc.Row(id="ventilation"),
                                                                                                     html.Hr(className="my-2"),  
                                                                                                     html.H5("Heating", className="card-title"),
                                                                                                     dbc.Row(id="heating"),
                                                                                                     html.Hr(className="my-2"),  
                                                                                                     html.H5("Refrigeration", className="card-title"),
                                                                                                     dbc.Row(id="refrigeration"),
                                                                                                    
                                                                                             ]),
                                                                                     ]),
                                                                            ]),
                                                                            ],                        
                                                                            id="popover_climat",
                                                                            is_open=False,
                                                                            target="button_popover_climat",
                                                                            placement="top",
                                                                    ),
                                                            ]),
                                                    ]),
                                                    dbc.Row([
                                                            dbc.Col(width={"size": 4, "offset":0}, children =[
                                                                html.H1(".", style={'color':'white'}),
                                                            ]),
                                                    ]),
                                                    dbc.Row([
                                                            dbc.Col(width={"size": 4, "offset":0}, children =[
                                                                html.H1(".", style={'color':'white'}),
                                                            ]),
                                                    ]),         
                                                    dbc.Row([
                                                            dbc.Col(width={"size": 3, "offset":7}, children =[
                                                                    dbc.Button(id="button_popover_inside", className="theme-bg2",children=[
                                                                            dbc.Badge(className="theme-bg" ,children=[
                                                                                    html.I(id="img_button_inside")
                                                                            ]),
                                                                            "   Inside",
                                                                    ]),
                                                                    dbc.Popover(children=[
                                                                            dbc.PopoverBody(className="theme-bg2 text-white",children=[
                                                                                     dbc.Card(className="card theme-bg text-white f-12", children=[
                                                                                             dbc.CardBody([
                                                                                                     html.H5("Temperature", className="card-title"),
                                                                                                     dbc.Row([
                                                                                                            dbc.Col(
                                                                                                                   html.I(className="fas fa-thermometer-half f-40", style={'color':'purple'}),
                                                                                                                   width={"size": 3, "offset": 1},
                                                                                                            ),        
                                                                                                            dbc.Col(
                                                                                                                   html.H3(id="in_temp",style={'color':'purple', "textAling":"center"}),
                                                                                                                   width={ "offset": 2},
                                                                                                            ),   
                                                                                                    ]),
                                                                                                     html.Hr(className="my-2"), 
                                                                                                     html.H5("Humidity", className="card-title"),
                                                                                                     dbc.Row([
                                                                                                            dbc.Col(
                                                                                                                   html.I(className="feather icon-download-cloud f-40", style={'color':'purple'}),
                                                                                                                   width={"size": 3, "offset": 1},
                                                                                                            ), 
                                                                                                            dbc.Col(
                                                                                                                   html.H3(id="in_hum",style={'color':'purple', "textAling":"center"}),
                                                                                                                   width={"size": "auto", "offset": 1},
                                                                                                            ),                                                            
                                                                                                            dbc.Col(), 
                                                                                                    ]),
                                                                                                     html.Hr(className="my-2"), 
                                                                                                     html.H5("Soil humidity", className="card-title"),
                                                                                                     dbc.Row([
                                                                                                            dbc.Col(
                                                                                                                   html.I(className="fas fa-tint f-38", style={'color':'purple'}),
                                                                                                                   width={"size": 3, "offset": 1},
                                                                                                            ),                                                              
                                                                                                            dbc.Col(
                                                                                                                   html.H3(id="soil_hum",style={'color':'purple', "textAling":"center"}),
                                                                                                                   width={"size": "auto", "offset": 1},
                                                                                                            ), 
                                                                                                    ]),
                                                                                             ]),
                                                                                     ]),
                                                                            ]), 
                                                                            ],
                                                                            id="popover_inside",
                                                                            is_open=False,
                                                                            target="button_popover_inside",
                                                                            placement="right",
                                                                    ),
                                                            ]),
                                                    ]),       
                                                    dbc.Row([
                                                            dbc.Col(width={"size": 3, "offset":2}, children =[
                                                                    dbc.Button(id="button_popover_deposit", className="theme-bg2",children=[
                                                                            dbc.Badge(className="theme-bg" ,children=[
                                                                                    html.I(id="img_button_deposit")
                                                                            ]),
                                                                            "   Deposit",
                                                                    ]),
                                                                    dbc.Popover([
                                                                            dbc.PopoverBody(className="theme-bg2 text-white", children=[
                                                                                     dbc.Card(className="card theme-bg text-white f-12", children=[
                                                                                             dbc.CardBody(children=[
                                                                                                     html.H5("Water temperature", className="card-title"),
                                                                                                     dbc.Row([
                                                                                                            dbc.Col(
                                                                                                                   html.I(className="fas fa-thermometer-half f-40", style={'color':'purple'}),
                                                                                                                   width={"size": 3, "offset": 2},
                                                                                                            ),                                                             
                                                                                                            dbc.Col(html.H3(id="water_temp",style={'color':'purple', "textAling":"center"})), 
                                                                                                    ]),
                                                                                                     html.Hr(className="my-2"),  
                                                                                                     html.H5("Water pump", className="card-title"),
                                                                                                     dbc.Row(id="pump"),
                                                                                             ]),
                                                                                     ]),
                                                                            ]),
                                                                        ],
                                                                        id="popover_deposit",
                                                                        is_open=False,
                                                                        target="button_popover_deposit",
                                                                        placement="left",
                                                                    ),
                                                            ]),
                                                    ]),
                                             ]), 
                                    ),   
                            ),
                    ]),
             ]), 
        ]
                                                                                                            
    else:
        layout = [  
            dbc.Card(className="card rides-card",style={'background':'#303435'}, children=[
                    dbc.CardBody([
                            dbc.Card(
                                    dbc.CardBody(
                                            html.Div(style={'background-image':'url(/assets/images/maqueta2.jpg)','background-repeat': 'no-repeat','height':'590px','width':'780px'}, children=[ 
                                                    dbc.Row([
                                                            dbc.Col(width={"size": 4, "offset":0}, children =[
                                                                 dbc.Card(className="card theme-bg text-white f-12", children=[
                                                                         html.H3("Greenhouse_1", style={'text-align':'center'}),
                                                                 ]),
                                                            ]),
                                                    ]),        
                                                    dbc.Row(justify="center", children=[
                                                            dbc.Alert("Gateway disconnected. No information available", color="warning"),
                                                    ]),
                                            ]),
                                    ),
                            ),
                    ]),
            ]),
        ]                    
                                                                                                        
    return layout