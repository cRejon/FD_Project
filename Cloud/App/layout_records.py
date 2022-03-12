# -*- coding: utf-8 -*-
import dash_bootstrap_components as dbc
import dash_html_components as html
import dash_core_components as dcc

from datetime import date
from datetime import timedelta



def serve_records_layout():
    
    layout = [
             html.Div(className="col-md-8 col-xl-12", children=[ 
                     dbc.Container(className="card theme-bg2 text-white f-12", children=[
                             dbc.Row(children=[
                                     dbc.Col(width={"size": 4, "offset":4}, children=[
                                             dbc.Card(className="card theme-bg text-white f-12", children=[
                                                html.H4("InfluxDB", style={'padding':'5px','text-align':'center'}),
                                             ]),
                                     ]),
                             ]), 
                             dbc.Row(children=[
                                     dbc.Col(width={"size": 12}, children=[
                                             dbc.Card(className="card theme-bg text-white f-12", children=[
                                                     dbc.CardHeader(
                                                             dbc.Row(no_gutters=True, align='center', children=[
                                                                    dbc.Col(width={"size": 3}, children=[
                                                                            html.H2("Greenhouse_1"),
                                                                    ]),
                                                                    dbc.Col(width={"size": 4, "offset": 2}, align="right", children=[
                                                                            dcc.DatePickerRange( 
                                                                                        id='date_selection',
                                                                                        max_date_allowed=date.today()+timedelta(days=1),
                                                                                        start_date=date.today()-timedelta(days=1),
                                                                                        end_date=date.today(),
                                                                                        first_day_of_week=1,
                                                                                        display_format='D/M/Y',
                                                                            ),                                                                    
                                                                    ]),
                                                                    dbc.Col(width={"size": 3}, children=[
                                                                            dbc.Button("Make inquiry", id="button_make_inquiry", size="md", block=True, outline=True, color="light"),
                                                                    ]),
                                                             ])
                                                     ),                                                                               
                                                     dbc.CardBody([  
                                                             dbc.Row(style={'padding-bottom':'10px'},children=[
                                                                    dbc.Col(width={"size": 12}, children=[
                                                                            html.H3("Nodes", style={'font-style': 'italic', 'text-align':'center'})
                                                                    ]),
                                                             ]),
                                                             dbc.Row(children=[
                                                                    dbc.Col(width={"size": 3}, children=[
                                                                            html.H5("Inside",style={'text-align':'center'})
                                                                    ]),
                                                                    dbc.Col(width={"size": 3}, children=[
                                                                            html.H5("Outside",style={'text-align':'center'})
                                                                    ]),
                                                                    dbc.Col(width={"size": 3}, children=[
                                                                            html.H5("Deposit",style={'text-align':'center'})
                                                                    ]),
                                                                    dbc.Col(width={"size": 3}, children=[
                                                                            html.H5("Climat",style={'text-align':'center'})
                                                                    ]),
                                                             ]),
                                                             dbc.Row(children=[
                                                                    dbc.Col(width={"size": 3}, children=[
                                                                            dcc.Dropdown(
                                                                                    id='dropdown_inside',
                                                                                    options=[
                                                                                        {'label': 'Temperature', 'value': 'in_temp'},
                                                                                        {'label': 'Humidity', 'value': 'in_hum'},
                                                                                        {'label': 'Soil humidity', 'value': 'soil_hum'},
                                                                                    ],
                                                                                    style={'color':'blue'},
                                                                                    multi=True,
                                                                            ),
                                                                    ]),
                                                                    dbc.Col(width={"size": 3}, children=[
                                                                            dcc.Dropdown(
                                                                                    id='dropdown_outside',
                                                                                    options=[
                                                                                        {'label': 'Temperature', 'value': 'out_temp'},
                                                                                        {'label': 'Humidity', 'value': 'out_hum'},
                                                                                        {'label': 'Door', 'value': 'door'},
                                                                                    ],
                                                                                    style={'color':'blue'},
                                                                                    multi=True,
                                                                            ),
                                                                    ]),
                                                                    dbc.Col(width={"size": 3}, children=[
                                                                            dcc.Dropdown(
                                                                                    id='dropdown_deposit',
                                                                                    options=[
                                                                                        {'label': 'Water temperature', 'value': 'water_temp'},
                                                                                        {'label': 'Pump', 'value': 'pump'},
                                                                                    ],
                                                                                    style={'color':'blue'},
                                                                                    multi=True,
                                                                            ),
                                                                    ]),
                                                                    dbc.Col(width={"size": 3}, children=[
                                                                            dcc.Dropdown(
                                                                                    id='dropdown_climat',
                                                                                    options=[
                                                                                        {'label': 'Ventilation', 'value': 'ventilation'},
                                                                                        {'label': 'Heating', 'value': 'heating'},
                                                                                        {'label': 'Refrigeration', 'value': 'refrigeration'},
                                                                                    ],
                                                                                    style={'color':'blue'},
                                                                                    multi=True,
                                                                            ),
                                                                    ]),
                                                             ]), 
                                                             html.Hr(style={'padding-bottom':'20px'}),                        
                                                             dbc.Row(style={'padding-bottom':'10px'}, children=[
                                                                    dbc.Col(width={"size": 12}, children=[
                                                                            html.H3("Control", style={'font-style': 'italic', 'text-align':'center'})
                                                                    ]),
                                                             ]),
                                                             dbc.Row(children=[
                                                                    dbc.Col(width={"size": 4, 'offset':2}, children=[
                                                                            html.H5("Irrigation",style={'text-align':'center'})
                                                                    ]),
                                                                    dbc.Col(width={"size": 4}, children=[
                                                                            html.H5("Climat",style={'text-align':'center'})
                                                                    ]),
                                                             ]),
                                                             dbc.Row(children=[
                                                                    dbc.Col(width={"size": 4, 'offset':2}, children=[
                                                                            dcc.Dropdown(
                                                                                    id='dropdown_irrigation_control',
                                                                                    options=[
                                                                                        {'label': 'Activation humidity', 'value': 'min_soil_hum'},
                                                                                        {'label': 'Irrigation time', 'value': 'irrig_time'},
                                                                                    ],
                                                                                    style={'color':'blue'},
                                                                                    multi=True,
                                                                            ),
                                                                    ]),
                                                                    dbc.Col(width={"size": 4}, children=[
                                                                            dcc.Dropdown(
                                                                                    id='dropdown_control_climat',
                                                                                    options=[
                                                                                        {'label': 'Minimum temperature', 'value': 'min_temp'},
                                                                                        {'label': 'Target temperature', 'value': 'target_temp'},
                                                                                        {'label': 'Maximum temperature', 'value': 'max_temp'},
                                                                                        {'label': 'Minimum humidity', 'value': 'min_hum'},
                                                                                        {'label': 'Maximum humidity', 'value': 'max_hum'},
                                                                                    ],
                                                                                    style={'color':'blue'},
                                                                                    multi=True,
                                                                            ),
                                                                    ]),
                                                             ]), 
                                                    ]),
                                            ]),
                                     ]),       
                             ]),
                             dcc.Loading(type='cube', color="#1DE9B6", children=[                                                       
                                     dbc.Row(children=[
                                             dbc.Col(width={"size": 12}, children=[
                                                     dbc.Card(className="card theme-bg2 text-white f-12", children=[
                                                             html.Div(id="graph"),
                                                     ]),
                                             ]),
                                     ]),
                                     dbc.Row(children=[
                                             dbc.Col(width={"size": 12}, children=[
                                                     dbc.Card(className="card theme-bg text-white", children=[
                                                        dbc.Table(id="sensors_table", style= {'font-size': '17px', 'font-weight':'lighter'})
                                                     ]),
                                             ]),
                                     ]),
                                     dbc.Row(children=[
                                             dbc.Col(width={"size": 12}, children=[
                                                     dbc.Card(className="card theme-bg text-white", children=[
                                                        dbc.Table(id="actuators_table", style= {'font-size': '17px', 'font-weight':'lighter'})
                                                     ]),
                                             ]),
                                     ]),
                             ]),                                               
                     ]), 
             ]),                               
              
    ]
    return layout
