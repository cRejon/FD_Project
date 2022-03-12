# -*- coding: utf-8 -*-
import dash_bootstrap_components as dbc
import dash_html_components as html
import dash_core_components as dcc

import paho.mqtt.subscribe as subscribe

from layout import get_gateway_connection

import json

IP_GETAWAY = open("./ip_getaway.txt", "r").read()


def serve_control_layout():
    
    control_state = {}
    gateway_connected = get_gateway_connection()
    
    if gateway_connected == True:        
        for system in ["irrigation", "climatControl"]:
            control_state[system] = json.loads(str(subscribe.simple("greenhouse1/{}".format(system), hostname= IP_GETAWAY, retained=True).payload).split("'")[1])
    
    layout = [
        dcc.Interval(id='interval_control', interval=1*3000,n_intervals=0),
        html.Div(className="col-md-8 col-xl-12", children=[ 
                dbc.Card(className="card rides-card",style={'background':'#303435'}, children=[
                dbc.CardBody([
                         dbc.Card(style={'color':'white',"background": "linear-gradient(to left, #0FE3FB 0%, rgb(79, 172, 254) 100%)"}, children=[
                                 dbc.CardHeader(
                                         dbc.Row(children=[
                                                 dbc.Col(width={"size": 1}, children=[
                                                        dbc.Button(id="button_irrigation_control",size="sm",outline=True, color="light", children=[
                                                                        html.Div(className="fas fa-bars")
                                                        ]),
                                                ]),
                                                dbc.Col(width={"size": 4}, children=[
                                                        html.H4("Irrigation control", style={'font-weight': '400'}),
                                                ]),
                                                dbc.Col( width={"size": 4}, children=[
                                                         dbc.Toast(
                                                            "Message sent successfully",
                                                            id="toast_irrigation",
                                                            is_open=False,
                                                            body_style={'text-align':'right'},
                                                            duration=2500,
                                                            
                                                        ),
                                                        
                                                ]),
                                                dbc.Col(width={"size": 3}, children=[
                                                        dbc.Button("Send updated data", id="button_update_irrigation_control", size="sm", block=True, outline=True, color="light"),
                                                ]),
                                         ])
                                 ),
                                 dbc.Collapse(id="collapse_irrigation_control", children=[
                                         dbc.CardBody([
                                                dbc.Row([
                                                        dbc.Col(width=5, children=
                                                                 html.H3("Current soil moisture"),
                                                        ),
                                                        dbc.Col(width=2,style={'text-align': 'center'},children=
                                                                html.H3(id="irrig_soil_hum"),
                                                        ),
                                                        dbc.Col(
                                                        ),
                                                ]),
                                                html.Hr(className="my-2"),
                                                dbc.Row(style={'padding-top':'20px'}, children=[
                                                        dbc.Col(width={"size": 4,"offset": 1}, children=
                                                                html.H3("Activation humidity"),
                                                        ),
                                                        dbc.Col(width=2,id="tooltip_min_soil_hum", style={'text-align': 'center'},children=
                                                                html.H3(id="min_soil_hum"),
                                                        ), 
                                                        dbc.Tooltip(
                                                            "Use the slider bar to select this value",
                                                            target="tooltip_min_soil_hum",
                                                            placement='left',
                                                        ),
                                                        dbc.Col(
                                                            dcc.Slider(id='dcc_min_soil_hum',
                                                                       min=0,
                                                                       max=80,
                                                                       step=5,
                                                                       value= control_state["irrigation"]["values"]["min_soil_hum"],
                                                                       included=False,
                                                                       updatemode="drag",
                                                                       marks={i: {'label': '{}%'.format(i), 'style': {'color': 'white'}} for i in range(0,100,20)}
                                                            )
                                                        ),   
                                                ]),
                                                dbc.Row(style={'padding-top':'25px'}, children=[
                                                        dbc.Col(width={"size": 4,"offset": 1},align='center', children=
                                                            html.H3("Irrigation time") 
                                                        ),
                                                        dbc.Col(width=2, children=
                                                                dbc.Input(
                                                                        type="number", 
                                                                        id="input_irrigation_seconds", 
                                                                        style={'color':'white','font-family': "inherit",'text-align': 'center','font-size':'180%','font-weight':'500',"background": "#30C6F9"}, 
                                                                        bs_size="lg", 
                                                                        value= control_state["irrigation"]["values"]["irrig_time"], 
                                                                        min=0, 
                                                                        max=300, 
                                                                        step=1),
                                                        ), 
                                                        dbc.Col(align='center', children=
                                                            html.H5("seconds") 
                                                        ),   
                                                ]),
                                       ]),
                               ]),
                         ]),                              
                         dbc.Card(className="card rides-card",style={'color':'white',"background": "linear-gradient(to left, rgb(240, 117, 199) 0%, rgb(145, 145, 255) 100%)"}, children=[
                                 dbc.CardHeader(
                                         dbc.Row([
                                                 dbc.Col(width={"size": 1}, children=[
                                                        dbc.Button(id="button_climatControl",size="sm",outline=True, color="light", children=[
                                                                        html.Div(className="fas fa-bars")
                                                        ]),
                                                ]),
                                                 dbc.Col(
                                                         html.H4("Climat Control", style={'font-weight': 'inherit'}),
                                                         width={"size": 4},
                                                ),
                                                 dbc.Col( width={"size": 4}, children=[
                                                         dbc.Toast(
                                                            "Message sent successfully",
                                                            id="toast_climatControl",
                                                            is_open=False,
                                                            body_style={'text-align':'right'},
                                                            duration=2500,
                                                        ),
                                                        
                                                ]),
                                                dbc.Col(width={"size": 3, "offset": 0}, children=[
                                                        dbc.Button("Send updated data", id="button_update_climatControl", size="sm", block=True, outline=True, color="light"),
                                                        
                                                ]),
                                        ])
                                 ),
                                 dbc.Collapse(id="collapse_climatControl", children=[
                                         dbc.CardBody([
                                                 dbc.Card(style={'color':'white',"background": "linear-gradient(to left, rgb(240, 117, 199) 0%, rgb(145, 145, 255) 100%)"}, children=[
                                                         dbc.CardHeader(
                                                                 dbc.Row([
                                                                         dbc.Col(width={"size": 1}, children=[
                                                                                dbc.Button(id="button_climatControl_temp",size="sm",outline=True, color="light", children=[
                                                                                                html.Div(className="fas fa-bars")
                                                                                ]),
                                                                        ]),
                                                                         dbc.Col(
                                                                                 html.H4("Temperature", style={'font-weight': 'inherit'}),
                                                                                 width={"size": 4},
                                                                        ),
                                                                ]),
                                                         ),
                                                         dbc.Collapse(id="collapse_climatControl_temp", children=[
                                                                 dbc.CardBody([                                                 
                                                                        dbc.Row(style={'padding-top':'5px','padding-left':'10px'}, children=[
                                                                                dbc.Col(width=5, children=
                                                                                        html.H3("Inside temperature"),
                                                                                ),
                                                                                dbc.Col(width=2,style={'text-align': 'center'},children=
                                                                                        html.H3(id="climatControl_in_temp")
                                                                                ),
                                                                                dbc.Col(
                                                                                ),
                                                                        ]),
                                                                        dbc.Row(style={'padding-left':'10px'}, children=[
                                                                                dbc.Col(width=5, children=
                                                                                        html.H3("Outside temperature"),
                                                                                ),
                                                                                dbc.Col(width=2,style={'text-align': 'center'},children=
                                                                                        html.H3(id="climatControl_out_temp")
                                                                                ),
                                                                                dbc.Col(
                                                                                ),
                                                                        ]),
                                                                        dbc.Row(justify="center",style={'padding-top':'20px', 'padding-bottom':'15px'}, children=[
                                                                                dbc.Col(width={"size": 5},id="tooltip_temp_range",align='center', children=
                                                                                    html.H3("Temperature range") 
                                                                                ),  
                                                                                dbc.Tooltip(
                                                                                        "The values ​​must be at least 3º apart",
                                                                                        target="tooltip_temp_range",
                                                                                        placement='left',
                                                                                ),
                                                                        ]),
                                                                        dbc.Row(no_gutters=True, children=[
                                                                                dbc.Col(width={"size": 1,"offset": 2} ,children=
                                                                                        html.H4("Min."),
                                                                                ),
                                                                                dbc.Col(width= 1,style={'text-align': 'center'},children=
                                                                                        html.H4(id="min_temp"),
                                                                                ),
                                                                                dbc.Col(width={"size": 1,"offset": 1},children=
                                                                                        html.H4("Targ."),
                                                                                ),
                                                                                dbc.Col(width=1,style={'text-align': 'center'},children=
                                                                                        html.H4(id="target_temp",style={'text-align':'left'}),
                                                                                ),
                                                                                dbc.Col(width={"size": 1,"offset": 1},children=
                                                                                        html.H4("Max.")
                                                                                ),
                                                                                dbc.Col(width=1,style={'text-align': 'center'},children=
                                                                                        html.H4(id="max_temp",style={'text-align':'left'}),
                                                                                ),
                                                                        ]),
                                                                        dbc.Row(style={'padding-top':'20px','padding-bottom':'20px'}, children=[
                                                                                dbc.Col(width={"size": 10,"offset": 1},align='center', children=
                                                                                        dcc.RangeSlider(
                                                                                                id='dcc_temp_range',
                                                                                                min=0,
                                                                                                max=40,
                                                                                                step=1,
                                                                                                value= [control_state["climatControl"]["values"]["min_temp"], control_state["climatControl"]["values"]["target_temp"], control_state["climatControl"]["values"]["max_temp"]],
                                                                                                pushable=3,
                                                                                                marks={i: {'label': '{}º'.format(i), 'style': {'color': 'white'}} for i in range(0,42,2)}
                                                                                        )
                                                                                )  
                                                                        ]),
                                                                ]),
                                                         ]),                               
                                                 ]),
                                                 dbc.Card(style={'color':'white',"background": "linear-gradient(to left, rgb(240, 117, 199) 0%, rgb(145, 145, 255) 100%)"}, children=[
                                                         dbc.CardHeader(
                                                                 dbc.Row([
                                                                         dbc.Col(width={"size": 1}, children=[
                                                                                dbc.Button(id="button_climatControl_hum",size="sm",outline=True, color="light", children=[
                                                                                                html.Div(className="fas fa-bars")
                                                                                ]),
                                                                        ]),
                                                                         dbc.Col(
                                                                                 html.H4("Humidity", style={'font-weight': 'inherit'}),
                                                                                 width={"size": 4},
                                                                        ),
                                                                ]),
                                                         ),
                                                         dbc.Collapse(id="collapse_climatControl_hum", children=[
                                                                 dbc.CardBody([ 
                                                                        dbc.Row(style={'padding-top':'5px','padding-left':'10px'}, children=[
                                                                                dbc.Col(width=4, children=
                                                                                        html.H3("Inside humidity"),
                                                                                ),
                                                                                dbc.Col(width=2,style={'text-align': 'center'},children=
                                                                                        html.H3(id="climatControl_in_hum"),
                                                                                ),
                                                                                dbc.Col(
                                                                                ),
                                                                        ]),
                                                                        dbc.Row(style={'padding-left':'10px'}, children=[
                                                                                dbc.Col(width=4, children=
                                                                                        html.H3("Outside humidity"),
                                                                                ),
                                                                                dbc.Col(width=2,style={'text-align': 'center'},children=
                                                                                        html.H3(id="climatControl_out_hum"),
                                                                                ),
                                                                                dbc.Col(
                                                                                ),
                                                                        ]),
                                                                        dbc.Row(justify="center",style={'padding-top':'20px', 'padding-bottom':'15px'}, children=[
                                                                                dbc.Col(width={"size": 4},id="tooltip_hum_range",align='center', children=
                                                                                    html.H3("Humidity range") 
                                                                                ),   
                                                                                dbc.Tooltip(
                                                                                        "The values ​​must be separated by at least 10%",
                                                                                        target="tooltip_hum_range",
                                                                                        placement='left',
                                                                                ), 
                                                                        ]),
                                                                        dbc.Row(no_gutters=True, children=[
                                                                                dbc.Col(width={"size": 1,"offset": 3} ,children=
                                                                                        html.H4("Min."),
                                                                                ),
                                                                                dbc.Col(width=1,children=
                                                                                        html.H4(id="min_hum",style={'text-align':'left'}),
                                                                                ),
                                                                                dbc.Col(width={"size": 1,"offset": 2},children=
                                                                                        html.H4("Max."),
                                                                                ),
                                                                                dbc.Col(width=1,children=
                                                                                        html.H4(id="max_hum",style={'text-align':'left'}),
                                                                                ),
                                                                        ]),
                                                                        dbc.Row(style={'padding-top':'20px','padding-bottom':'20px'}, children=[
                                                                                dbc.Col(width={"size": 10,"offset": 1},align='center', children=
                                                                                        dcc.RangeSlider(
                                                                                        id='dcc_hum_range',
                                                                                        min=10,
                                                                                        max=90,
                                                                                        step=1,
                                                                                        value= [control_state["climatControl"]["values"]["min_hum"], control_state["climatControl"]["values"]["max_hum"]],
                                                                                        pushable=10,
                                                                                        updatemode= 'drag',
                                                                                        marks={i: {'label': '{}º'.format(i), 'style': {'color': 'white'}} for i in range(10,100,10)})
                                                                                ),
                                                                        ]),                                                                 
                                                                ]),
                                                         ]),                               
                                                 ]),
                                         ]),
                                 ]),
                         ]),
                 ]),
                 ]),                                                                       
         ]),                          
            
    ]
    
    return layout