# -*- coding: utf-8 -*-
import paho.mqtt.subscribe as subscribe
import paho.mqtt.publish as publish

import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
import callbacks

from app import app
import layout


app.layout = layout.serve_layout

server= app.server

if __name__ == '__main__':
    app.run_server(debug=False)