# -*- coding: utf-8 -*-
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html

import paho.mqtt.subscribe as subscribe


IP_GETAWAY = open("./ip_getaway.txt", "r").read()

gateway_connected = False

def get_gateway_connection():
    global gateway_connected
    
    return gateway_connected

def serve_layout():
    global gateway_connected
    
    disconnection_alert = None
    
    try:
        subscribe.simple("greenhouse1/estate/inside", hostname= IP_GETAWAY, retained=True)
        gateway_connected = True
        
    except:
        disconnection_alert =  dbc.Alert("Attention! Unable to connect to the gateway. Check the Internet connection of the device", color="danger"),
    
    
    layout =  html.Div(style={'backgroundColor':'#f4f7fa'},children=[
        dcc.Location(id="url"),
# Page header
        html.Header(className="navbar pcoded-header navbar-expand-lg navbar-light header-dark", children=[
                    html.Div(className="collapse navbar-collapse", children=[
                            dbc.Row(justify="center", children= disconnection_alert),        
                            
                    ]),
        ]),

# Lateral menu
        dbc.Nav(className="pcoded-navbar brand-dark navbar-dark", children=
                html.Div(className="navbar-wrapper", children=[
                        html.Div(className="navbar-brand header-logo", children=[
                                html.A(className="b-brand", children=[
                                         html.Div(className="b-bg", children=[
                                                 html.I(className="feather icon-codepen", children=[ ]),
                                         ]),
                                         html.Span(className="b-title", children= "IoT platform"),                                        
                                ]),
                        ]),
                        html.Div(className="navbar-content scroll-div", children=[
                                html.Ul(className="nav pcoded-inner-navbar", children=[
                                        html.Li(className="nav-item pcoded-menu-caption", children=[
                                                html.Label("Navigation")
                                        ]),
                                        html.Li(className="nav-item", children=[
                                                        dbc.NavLink(className="nav-link",href="/facilities", children=[
                                                               html.Span(className="pcoded-micon", children=[
                                                                       html.I(className="feather icon-home", children=[
                                                                       ])
                                                               ]),
                                                               html.Span(className="pcoded-mtext", children="Facilities"),
                                                        ]),                                                               
                                        ]),   
                                        html.Li(className="nav-item", children=[
                                                        dbc.NavLink(className="nav-link",href="/devices", children=[
                                                               html.Span(className="pcoded-micon", children=[
                                                                       html.I(className="feather icon-radio", children=[
                                                                       ])
                                                               ]),
                                                               html.Span(className="pcoded-mtext", children="Devices"),
                                                        ]),                                                               
                                        ]),    
                                        html.Li(className="nav-item", children=[
                                                        dbc.NavLink(className="nav-link",href="/control-panel", children=[
                                                               html.Span(className="pcoded-micon", children=[
                                                                       html.I(className="fas fa-sliders-h", children=[
                                                                       ])
                                                               ]),
                                                               html.Span(className="pcoded-mtext", children="Control Panel"),
                                                        ]),                                                               
                                        ]), 
                                        html.Li(className="nav-item", children=[
                                                        dbc.NavLink(className="nav-link",href="/records", children=[
                                                               html.Span(className="pcoded-micon", children=[
                                                                       html.I(className="fas fa-database", children=[
                                                                       ])
                                                               ]),
                                                               html.Span(className="pcoded-mtext", children="Records"),
                                                        ]),                                                               
                                        ]),  
                                ]),
                                html.Div(className="ps__rail-x", style={'left':'0px', 'bottom':'0px'}, children=[
                                        html.Div(className="ps__thumb-x", tabIndex='0', style={'left':'0px', 'width':'0px'}),
                                ]),
                                html.Div(className="navbar-wrapper", style={'top':'0px', 'height':'587px', 'right':'0px'}, children=[
                                        html.Div(className="ps__thumb-y", tabIndex='0', style={'top':'0px', 'height':'160px'}),
                                ]),
                        ]),
                ]),
          ),
# Page body
          html.Div(className="pcoded-main-container", children=[
                    html.Div(className="pcoded-wrapper", children=[
                            html.Div(className="pcoded-content", children=[
                                    html.Div(className="pcoded-inner-content", children=[
                                             html.Div(className="main-body", children=[
                                                     html.Div(className="page-wrapper", children=[
                                                             html.Div(id= "body",className="row", children=[]),
                                                     ]),
                                             ]),
                                    ]),
                            ]),
                    ]),
            ]),  
    ]) 

    return layout  

