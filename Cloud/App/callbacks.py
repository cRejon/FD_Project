# -*- coding: utf-8 -*-
from more_itertools import difference
import paho.mqtt.publish as publish

import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output, State
import dash_bootstrap_components as dbc

import json
import pandas as pd
import datetime as dt
import pytz
from math import log10, floor

import plotly.graph_objs as go

from pinform.client import InfluxClient
from ORM_influxdb import Inside, Outside, Deposit, Climat, Irrigation, ClimatControl



from layout import get_gateway_connection

import layout_facilities
import layout_control_panel
import layout_devices
import layout_records

from app import app

IP_GETAWAY = open("./ip_getaway.txt", "r").read()

def icon_door_conversor(measure):
    if measure == 0:
        return [
                dbc.Col(width={"size": 1, "offset": 0}, children=[html.I(className="fas fa-door-closed  f-36", style={'color':'purple'})]),                                                             
                dbc.Col(width={"size": 8, "offset": 2}, children=[html.H4("closed",style={'color':'purple', "textAling":"right"})]), 
                ]
    else:
        return [
                dbc.Col(width={"size": 1, "offset": 0}, children=[html.I(className="fas fa-door-open  f-36", style={'color':'purple'})]),                                                             
                dbc.Col(width={"size": 8, "offset": 2}, children=[html.H4("open",style={'color':'purple', "textAling":"right"})]), 
                ]
        
def icon_actuators_conversor(measure):
    if measure == 0:
        return [
                dbc.Col(width={"size": 2, "offset":1}, children =[html.I(className="feather icon-x-circle f-38", style={'color':'purple'})]),                                                            
                dbc.Col(width={ "offset":2}, children =[html.H3("OFF", style={'color':'purple', "textAling":"center"})])
                ]
    else:
        return [
                dbc.Col(width={"size": 2, "offset":1}, children =[html.I(className="feather icon-check f-38", style={'color':'purple'})]),                                                            
                dbc.Col(width={ "offset":2}, children =[html.H3("ON", style={'color':'purple', "textAling":"center"})])
                ]



# Page changed
@app.callback(Output("body", "children"), [Input("url", "pathname")])
def render_page_content(pathname):
    if pathname in ["/", "/facilities"]:
        return layout_facilities.serve_facilities_layout()
    elif pathname == "/devices":
        return layout_devices.serve_devices_layout()
    elif pathname == "/control-panel":
        return layout_control_panel.serve_control_layout()
    elif pathname == "/records":
        return layout_records.serve_records_layout()
    # If the user tries to reach a different page, return a 404 message
    return dbc.Jumbotron(
        [
            html.H1("404: Not found", className="text-danger"),
            html.Hr(),
            html.P("The address {} has not been recognized...".format(pathname)),
        ]
    )


# Callback to update inside node 
@app.callback([Output('button_popover_inside', 'disabled'),
              Output('img_button_inside', 'className'),
              Output('in_temp', 'children'),
              Output('in_hum', 'children'),
              Output('soil_hum', 'children')],
              [Input('interval_facilities', 'n_intervals')])
def update_inside_node(n_intervals):
    gateway_connected = get_gateway_connection()
    
    if gateway_connected == True:
        with open("./inside.txt", "r") as file:
                state = json.loads(file.read())         

        if state["signal"] == "disconnected":
            return [True, "feather icon-wifi-off f-20", None, None, None ]
        else:
            return [False, 
                    "feather icon-wifi f-20", 
                    (str(state["values"].get("in_temp"))+"ºC"),
                    (str(state["values"].get("in_hum"))+"%"),
                    (str(state["values"].get("soil_hum"))+"%")]
            
            
# Callback to update outside node
@app.callback([Output('button_popover_outside', 'disabled'),
              Output('img_button_outside', 'className'),
              Output('out_temp', 'children'),
              Output('out_hum', 'children'),
              Output('door', 'children')],
              [Input('interval_facilities', 'n_intervals')])
def update_outside_node(n_intervals):
    gateway_connected = get_gateway_connection()
    
    if gateway_connected == True:
        with open("./outside.txt", "r") as file:
                state = json.loads(file.read())         

        if state["signal"] == "disconnected":
            return [True, "feather icon-wifi-off f-20", None, None, None ]
        else:
            return [False, 
                    "feather icon-wifi f-20", 
                    (str(state["values"].get("out_temp"))+"ºC"),
                    (str(state["values"].get("out_hum"))+"%"),
                    icon_door_conversor(state["values"].get("door"))]
            

# Callback to update deposit node
@app.callback([Output('button_popover_deposit', 'disabled'),
              Output('img_button_deposit', 'className'),
              Output('water_temp', 'children'),
              Output('pump', 'children')],
              [Input('interval_facilities', 'n_intervals')])
def update_deposit_node(n_intervals):
    gateway_connected = get_gateway_connection()
    
    if gateway_connected == True:
        with open("./deposit.txt", "r") as file:
                state = json.loads(file.read())         

        if state["signal"] == "disconnected":
            return [True, "feather icon-wifi-off f-20", None, None ]
        else:
            return [False, 
                    "feather icon-wifi f-20", 
                    (str(state["values"].get("water_temp"))+"ºC"),
                    icon_actuators_conversor(state["values"].get("pump"))]
  
    
# Callback to update climat node         
@app.callback([Output('button_popover_climat', 'disabled'),
              Output('img_button_climat', 'className'),
              Output('ventilation', 'children'),
              Output('heating', 'children'),
              Output('refrigeration', 'children')],
              [Input('interval_facilities', 'n_intervals')])
def update_climat_node(n_intervals):
    gateway_connected = get_gateway_connection()
    
    if gateway_connected == True:
        with open("./climat.txt", "r") as file:
                state = json.loads(file.read())         

        if state["signal"] == "disconnected":
            return [True, "feather icon-wifi-off f-20", None, None, None ]
        else:
            return [False, 
                    "feather icon-wifi f-20", 
                    icon_actuators_conversor(state["values"].get("ventilation")),
                    icon_actuators_conversor(state["values"].get("heating")),
                    icon_actuators_conversor(state["values"].get("refrigeration"))]
            
            
# Callback to update irrigation control
@app.callback([Output('button_irrigation_control', 'disabled'),
              Output('button_update_irrigation_control', 'disabled'),
              Output('irrig_soil_hum', 'children')],
              [Input('interval_control', 'n_intervals')])
def update_irrigation_control(n_intervals):
    gateway_connected = get_gateway_connection()
    
    if gateway_connected == True:
        with open("./inside.txt", "r") as file:
            state = json.loads(file.read())         

        if state["signal"] == "disconnected":
            return [True, True, None]
        
        else:
            return [False, False,(str(state["values"].get("soil_hum"))+"%")]
        
    else:
        return [True, True, None]
        
        
# Callback to update climat control 
@app.callback([Output('button_climatControl', 'disabled'),
              Output('button_update_climatControl', 'disabled'),
              Output('climatControl_in_temp', 'children'),
              Output('climatControl_out_temp', 'children'),
              Output('climatControl_in_hum', 'children'),
              Output('climatControl_out_hum', 'children')],
              [Input('interval_control', 'n_intervals')])
def update_climat_control(n_intervals):
    gateway_connected = get_gateway_connection()
    global_state = {}
    
    if gateway_connected == True:
        for node in ["inside", "outside"]:
            with open("./{}.txt".format(node), "r") as file:
                global_state[node] = json.loads(file.read())         

            if global_state[node]["signal"] == "disconnected":
                return [True, True, None, None, None, None]
        
        return [False, 
                False,
                str(global_state["inside"]["values"]["in_temp"])+"ºC",
                str(global_state["outside"]["values"]["out_temp"])+"ºC",
                str(global_state["inside"]["values"]["in_hum"])+"%",
                str(global_state["outside"]["values"]["out_hum"])+"%"]
        
    else:
        return [True, True, None, None, None, None]
        
            
# Toggle for popover elements
for node in ["inside","outside", "deposit", "climat"]:
    @app.callback(
        Output("popover_{}".format(node), "is_open"),
        [Input("button_popover_{}".format(node), "n_clicks")],
        [State("popover_{}".format(node), "is_open")])
    def toggle_popover(n, is_open):
        if n:
            return not is_open
        return is_open


# Toggle for collapse elements 
for p in ["irrigation_control", "climatControl", "climatControl_temp", "climatControl_hum", "gateway_software"]:
    @app.callback(
        Output("collapse_{}".format(p), "is_open"),
        [Input("{}".format(p), "n_clicks")],
        [State("collapse_{}".format(p), "is_open")])
    def toggle_collapse(n, is_open):
        if n:
            return not is_open
        return is_open

# Toggle for modal elements
for node in ["inside", "outside", "deposit", "climat"]:
    @app.callback(
        Output("modal_{}".format(node), "is_open"),
        [Input("button_modal_{}".format(node), "n_clicks"), 
         Input("close_modal_{}".format(node), "n_clicks")],
        [State("modal_{}".format(node), "is_open")])
    def toggle_modal(n1, n2, is_open):
        if n1 or n2:
            return not is_open
        return is_open    

# Callback to visualize temperature range
@app.callback(
    [Output('min_temp', 'children'),
     Output('target_temp', 'children'),
    Output('max_temp', 'children')],
    [Input('dcc_temp_range', 'value')])
def visualize_temp_range(value):
    return  ['{}ºC'.format(value[0]),
             '{}ºC'.format(value[1]),
             '{}ºC'.format(value[2])]

# Callback to visualize humidity range
@app.callback(
    [Output('min_hum', 'children'),
     Output('max_hum', 'children')],
    [Input('dcc_hum_range', 'value')])
def visualize_hum_range(value):
    return ['{}%'.format(value[0]),
            '{}%'.format(value[1])]

# Callback to visualize minimum soil humidity
@app.callback(
    Output('min_soil_hum', 'children'),
    [Input('dcc_min_soil_hum', 'value')])
def get_soil_humidity(value):
    print(value)
    return '{}%'.format(value)

# Callback to send irrigation control values
@app.callback(
    Output('toast_irrigation', 'is_open'),
    [Input('button_update_irrigation_control', 'n_clicks')],
    [State('dcc_min_soil_hum','value'),
     State('input_irrigation_seconds','value')])
def send_irrigation_control(nClicks, min_soil_hum, irrig_time):
    if nClicks: # avoid the transient sending of a message when opening the app
        msg_dict ={}
        msg_dict["id"]="irrigation"
        msg_dict["values"]={}
        msg_dict["values"]["min_soil_hum"]=min_soil_hum
        msg_dict["values"]["irrig_time"]=irrig_time
        publish.single("greenhouse1/irrigation", payload= json.dumps(msg_dict), hostname= IP_GETAWAY, qos= 2, retain= True)
        return True
    else:
        return False

# Callback to send climat control values
@app.callback(
    Output('toast_climatControl', 'is_open'),
    [Input('button_update_climatControl', 'n_clicks')],
    [State('dcc_temp_range','value'),
     State('dcc_hum_range', 'value')])
def send_climatControl(nClicks, temp_range, hum_range):
    if nClicks: # avoid the transient sending of a message when opening the app
        msg_dict ={}
        msg_dict["id"]="climatControl"
        msg_dict["values"]={}
        msg_dict["values"]["min_temp"]=temp_range[0]
        msg_dict["values"]["target_temp"]=temp_range[1]
        msg_dict["values"]["max_temp"]=temp_range[2]
        msg_dict["values"]["min_hum"]=hum_range[0]
        msg_dict["values"]["max_hum"]=hum_range[1]
        publish.single("greenhouse1/climatControl", payload= json.dumps(msg_dict), hostname= IP_GETAWAY, qos= 2, retain= True)
        return True
    else:
        return False

# Callback to create the graph and statistics
@app.callback(
    [Output('graph', 'children'),
     Output('sensors_table', 'children'),
    Output('actuators_table', 'children')],
    [Input('button_make_inquiry', 'n_clicks')],
    [State('dropdown_inside','value'),
     State('dropdown_outside','value'),
     State('dropdown_deposit','value'),
     State('dropdown_climat', 'value'),
     State('dropdown_irrigation_control', 'value'),
     State('dropdown_climatControl', 'value'),
     State('date_selection', 'start_date'),
     State('date_selection', 'end_date')])
def create_graph_and_statistics(nClicks, inside_selec, outside_selec, deposit_selec, climat_selec, irrigation_control_selec, climatControl_selec, picker_start_date, picker_end_date):
    
    changer = {"in_temp": "Inside Temperature", "in_hum": "Inside humidity", "soil_hum": "Soil humidity","out_temp": "Outside Temperature", "out_hum": "Outside humidity", 
              "door": "Door", "water_temp": "Water temperature", "pump": "Pump", "ventilation": "Ventilation", "heating": "Heating", "refrigeration": "Refrigeration",
            "min_soil_hum":"Minimum soil humidity", "irrig_time": "Irrigation time", "min_temp": "Minimum temperature",
            "target_temp": "Target temperature", "max_temp": "Maximum Temperature", "min_hum": "Minimum humidity", "max_hum": "Maximum humidity"}
    
    hover_template_dict = {"in_temp":"%{y}ºC", "in_hum":"%{y}%", "soil_hum":"%{y}%", "out_temp":"%{y}ºC", "out_hum":"%{y}%", "door":"", "water_temp":"%{y}ºC" }

    if nClicks:  # avoid the transient sending of a message when opening the app
        client = InfluxClient(host="localhost", port=8086, username="pfg", password="password", database_name="greenhouse_1")
        start_date = dt.datetime.strptime(picker_start_date, '%Y-%m-%d')
        start_date = start_date.replace(tzinfo=pytz.utc)
        # if the last day is today, the current time is taken as the end time
        if picker_end_date == dt.datetime.now().strftime("%Y-%m-%d"):
            end_date = dt.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        else:
            end_date = picker_end_date + " 23:59:59"
        # need to convert the object from String to Datetime
        end_date = dt.datetime.strptime(end_date, '%Y-%m-%d %H:%M:%S')
        end_date = end_date.replace(tzinfo=pytz.utc)
        
        df = pd.DataFrame()
        
        figure=go.Figure()
        
        # tables to save the statistical values ​​of the sensors and operational values ​​of the actuators
        sensors_table =[]
        sensors_table_header=[]
        actuators_table =[]
        actuators_table_header=[]
        
        def add_sensor_trace(type):
            figure.add_trace(go.Scatter(x=(df.index+ dt.timedelta(hours=2)), y=df[type], name=changer[type], mode='markers+lines', line_shape='spline',
                                        hoverinfo="y", hovertemplate = hover_template_dict[type], marker={'size': 1, "opacity": 0.6, "line": {'width': 0.5}})) 
            
        def add_actuator_trace(type):
            figure.add_trace(go.Scatter(x=(df.index+ dt.timedelta(hours=2)), y=df[type], name=changer[type], mode='lines', line_shape='hv',
                                        hoverinfo="y", hovertemplate = None, line={'width': 2, 'dash':'dot'})) 
        
        def add_control_trace(type):  
            figure.add_trace(go.Scatter(x=(df.index+ dt.timedelta(hours=2)), y=df[type], name=changer[type], mode='lines', line_shape='hv',
                                        hoverinfo="y", hovertemplate = None, line={'width': 2, 'dash':'dashdot'})) 
        
        def create_sensors_table_row(type):
            statistics = pd.Series(df[type]).describe().round(1)
            sensors_table.append(html.Tr([html.Th(changer[type]), 
                                      html.Th(statistics.loc['mean'], style={'text-align':'center', 'color':'purple'}),
                                      html.Th(statistics.loc['std'], style={'text-align':'center', 'color':'purple'}), 
                                      html.Th(statistics.loc['min'], style={'text-align':'center', 'color':'purple'}), 
                                      html.Th(statistics.loc['25%'], style={'text-align':'center', 'color':'purple'}),
                                      html.Th(statistics.loc['50%'], style={'text-align':'center', 'color':'purple'}), 
                                      html.Th(statistics.loc['75%'], style={'text-align':'center', 'color':'purple'}), 
                                      html.Th(statistics.loc['max'], style={'text-align':'center', 'color':'purple'})]))
        
        def create_actuators_table_row(type):
            slots_rates = {"rate_slot_1":0.18569208, "rate_slot_2":0.09793349, "rate_slot_3":0.08394299} # dictionary with the rates of each time slot in €/kWh
            powers = {"pump":5, "ventilation":1, "heating":20, "refrigeration":60} # dictionary with the powers of the actuators in Watts
            slots_durations = {"duration_slot_1":0 , "duration_slot_2":0, "duration_slot_3":0} # dictionary with the time of use (in hours) in each time slot
            slots_energies = {"energy_slot_1":0 , "energy_slot_2":0, "energy_slot_3":0} # dictionary with the energy consumed (in kWh) in each time slot
            slots_costs = {"cost_slot_1":0 , "cost_slot_2":0, "cost_slot_3":0} # dictionary with the cost (in euros) in each time slot
        
            # DataFrame with time slots
            rates_by_hour_df = pd.DataFrame(index=range(0,24), columns=range(0,7))
            for day in range(0,7):
                # from 00:00 to 01:00 rate 2
                rates_by_hour_df.loc[0, day] = 2
                # from 01:00 to 07:00 rate 3
                for hour in range(1,7):
                    rates_by_hour_df.loc[hour, day] = 3
                # from 07:00 to 13:00 rate 2
                for hour in range(7,13):
                    rates_by_hour_df.loc[hour, day] = 2
                # from 13:00 to 23:00 rate 1
                for hour in range(13,23):
                    rates_by_hour_df.loc[hour, day] = 1
                # from 23:00 to 00:00 rate 2
                rates_by_hour_df.loc[23, day] = 2
             
            # get the moments where the actuators go from off to on and vice versa
            difference_serie = pd.Series(df[type]).diff()
            diff_series= difference_serie.where(difference_serie!=0).dropna()
            if diff_series.empty:
                diff_series = pd.Series([0])            
            
            # Dataframe with hours of the day as index, days of week (0-6) as columns, and Timedelta objects as values
            activated_time_df = pd.DataFrame(index=range(0,24), columns=range(0,7)).fillna(pd.Timedelta('00:00:00', unit='second'))
            
            # calculates the time of use in each time slot and each day
            if diff_series[0] == -100: # if the first value is off, we count the power on from 00:00
                lower_hour = start_date 
                while (lower_hour.hour != diff_series[0:1].index.hour[0]):
                    activated_time_df.loc[lower_hour.hour, lower_hour.weekday()] += pd.Timedelta('01:00:00')
                    lower_hour += pd.Timedelta('01:00:00')
                activated_time_df.loc[diff_series[0:1].index.hour, diff_series[0:1].index.weekday] = pd.Timedelta('00:{}:00'.format(diff_series[0:1].index.minute[0]), unit='second')           
        
            for p in range(diff_series.count()):
                if diff_series[p] == 100:
                    # avoid Out of Range error when the last value of the array is 100
                    if p+1 < diff_series.count():
                        # check if it turns on and off at the same hour
                        if (diff_series[p+1:p+2].index.hour[0] == diff_series[p:p+1].index.hour[0]) and (diff_series[p+1:p+2].index.date[0] == diff_series[p:p+1].index.date[0]):
                            parcial_duration = (diff_series[p+1:p+2].index[0]) - (diff_series[p:p+1].index[0])
                            activated_time_df.loc[diff_series[p:p+1].index.hour, diff_series[p:p+1].index.weekday] += parcial_duration 
                            
                        else:
                            # the ceil method rounds up the hour and changes the object to a Timestamp
                            upper_hour = diff_series[p:p+1].index[0].ceil(freq='H')
                            parcial_duration = upper_hour - diff_series[p:p+1].index[0]
                            activated_time_df.loc[diff_series[p:p+1].index.hour, diff_series[p:p+1].index.weekday] += parcial_duration 
                            
                            while (upper_hour.hour != diff_series[p+1:p+2].index.hour[0]) or (upper_hour.date() != diff_series[p+1:p+2].index.date[0]):
                                activated_time_df.loc[upper_hour.hour, upper_hour.weekday()] += pd.Timedelta('01:00:00')
                                upper_hour += pd.Timedelta('01:00:00')
                            
                            parcial_duration = (diff_series[p+1:p+2].index[0]) - upper_hour
                            activated_time_df.loc[upper_hour.hour, upper_hour.weekday()] += parcial_duration
                            
                    else:
                        if (end_date.hour == diff_series[p:p+1].index.hour[0]) and (end_date.date() == diff_series[p:p+1].index.date[0]):
                            parcial_duration = end_date - diff_series[p:p+1].index[0]
                            activated_time_df.loc[diff_series[p:p+1].index.hour, diff_series[p:p+1].index.weekday] += parcial_duration 
                            
                        else:
                            # the ceil method rounds up the hour and changes the object to a Timestamp
                            upper_hour = diff_series[p:p+1].index[0].ceil(freq='H')
                            parcial_duration = upper_hour - diff_series[p:p+1].index[0]
                            activated_time_df.loc[diff_series[p:p+1].index.hour, diff_series[p:p+1].index.weekday] += parcial_duration 
                            
                            while upper_hour.hour != end_date.hour or (upper_hour.date() != end_date.date()):
                                activated_time_df.loc[upper_hour.hour, upper_hour.weekday()] += pd.Timedelta('01:00:00')
                                upper_hour += pd.Timedelta('01:00:00')
                            
                            parcial_duration = (end_date + dt.timedelta(seconds=1)) - upper_hour
                            activated_time_df.loc[upper_hour.hour, upper_hour.weekday()] += parcial_duration
        
            # calculate time in each slot
            for day in range(0,7):
                for hour in range(0,24):
                    for slot in range(1,4):
                        if rates_by_hour_df.loc[hour, day] == slot:
                            slots_durations["duration_slot_{}".format(slot)] += activated_time_df.loc[hour, day].total_seconds()/3600
            
            # calculate energies in each slot
            for slot in range(1,4):
                slots_energies["energy_slot_{}".format(slot)] = slots_durations["duration_slot_{}".format(slot)] * powers[type]
                
            # calculate costs in each slot
            for slot in range(1,4):
                slots_costs["cost_slot_{}".format(slot)] = slots_energies["energy_slot_{}".format(slot)] * (slots_rates["rate_slot_{}".format(slot)] / 1000)
            
            # round to the most significant figure chosen
            def round_to_n(number, n):
                if number != 0:
                    return round(number, (n-1) -int(floor(log10(abs(number)))))
                else:
                    return 0
            
            # round values
            for slot in range(1,4):
                    slots_durations["duration_slot_{}".format(slot)] = round(slots_durations["duration_slot_{}".format(slot)],2)
                    slots_energies["energy_slot_{}".format(slot)] = round_to_n (slots_energies["energy_slot_{}".format(slot)],3)
                    slots_costs["cost_slot_{}".format(slot)] = round_to_n (slots_costs["cost_slot_{}".format(slot)],2)

            # total values 
            total_time = round (slots_durations["duration_slot_1"] + slots_durations["duration_slot_2"] + slots_durations["duration_slot_3"], 2)
            total_energy = round_to_n (slots_energies["energy_slot_1"] + slots_energies["energy_slot_2"] + slots_energies["energy_slot_3"], 3)
            total_cost = round_to_n (slots_costs["cost_slot_1"] + slots_costs["cost_slot_2"] + slots_costs["cost_slot_3"], 2)

            # add the values ​​to the table
            actuators_table.append(html.Tr([html.Th(changer[type], rowSpan=("4"), style={'vertical-align':'middle'}), 
                                      html.Th("1", style={'text-align':'center', 'color':'purple'}),
                                      html.Th(slots_durations["duration_slot_1"], style={'text-align':'center', 'color':'purple'}), 
                                      html.Th(slots_energies["energy_slot_1"], style={'text-align':'center', 'color':'purple'}), 
                                      html.Th(slots_costs["cost_slot_1"], style={'text-align':'center', 'color':'purple'})]))
            actuators_table.append(html.Tr([     
                                      html.Th("2", style={'text-align':'center', 'color':'purple'}),
                                      html.Th(slots_durations["duration_slot_2"], style={'text-align':'center', 'color':'purple'}), 
                                      html.Th(slots_energies["energy_slot_2"], style={'text-align':'center', 'color':'purple'}), 
                                      html.Th(slots_costs["cost_slot_2"], style={'text-align':'center', 'color':'purple'})]))
            actuators_table.append(html.Tr([     
                                      html.Th("3", style={'text-align':'center', 'color':'purple'}),
                                      html.Th(slots_durations["duration_slot_3"], style={'text-align':'center', 'color':'purple'}), 
                                      html.Th(slots_energies["energy_slot_3"], style={'text-align':'center', 'color':'purple'}), 
                                      html.Th(slots_costs["cost_slot_3"], style={'text-align':'center', 'color':'purple'})]))
            actuators_table.append(html.Tr([     
                                      html.Th("Total", style={'text-align':'center', 'color':'purple'}),
                                      html.Th(total_time, style={'text-align':'center', 'color':'purple'}), 
                                      html.Th(total_energy, style={'text-align':'center', 'color':'purple'}), 
                                      html.Th(total_cost, style={'text-align':'center', 'color':'purple'})]))



        if inside_selec:
            # create a dictionary of keys just to pass to the influxDB client
            selection = {}
            for elements in inside_selec:
                selection[elements] = ""
                
            df = pd.DataFrame.from_dict(client.get_fields_as_series(Inside ,selection ,time_range= (start_date,end_date)))
            for type in inside_selec:
                add_sensor_trace(type)   
                create_sensors_table_row(type)
            
        if outside_selec:
            selection = {}
            for elements in outside_selec:
                selection[elements] = ""
                
            df = pd.DataFrame.from_dict(client.get_fields_as_series(Outside ,selection ,time_range= (start_date,end_date)))
            for type in outside_selec:
                if type in ("out_temp", "out_hum"):
                    add_sensor_trace(type)
                    create_sensors_table_row(type)
                if type in ("door"):
                    add_actuator_trace(type)
                    
        if deposit_selec:
            selection = {}
            for elements in deposit_selec:
                selection[elements] = ""
                
            df = pd.DataFrame.from_dict(client.get_fields_as_series(Deposit ,selection ,time_range= (start_date,end_date)))
            for type in deposit_selec:
                if type in ("water_temp"):
                    add_sensor_trace(type)
                    create_sensors_table_row(type)
                if type in ("pump"):
                    add_actuator_trace(type)
                    create_actuators_table_row(type)
                    
        if climat_selec:
            selection = {}
            for elements in climat_selec:
                selection[elements] = ""
                
            df = pd.DataFrame.from_dict(client.get_fields_as_series(Climat ,selection ,time_range= (start_date,end_date)))
            for type in climat_selec:
                add_actuator_trace(type)
                create_actuators_table_row(type)
                
        if irrigation_control_selec:
            selection = {}
            for elements in irrigation_control_selec:
                selection[elements] = ""
                
            df = pd.DataFrame.from_dict(client.get_fields_as_series(Irrigation ,selection ,time_range= (start_date,end_date)))
            for type in irrigation_control_selec:
                add_control_trace(type)    
          
        if climatControl_selec:
            selection = {}
            for elements in climatControl_selec:
                selection[elements] = ""
                
            df = pd.DataFrame.from_dict(client.get_fields_as_series(ClimatControl ,selection ,time_range= (start_date,end_date)))
            for type in climatControl_selec:
                add_control_trace(type)       
        
        if sensors_table:
            sensors_table_header = [html.Thead(html.Tr([html.Th(""), 
                                       html.Th("Mean", style={'text-align':'center'}),
                                       html.Th("Standard deviation", style={'text-align':'center'}), 
                                       html.Th("Minimum", style={'text-align':'center'}),
                                       html.Th("1st quartile", style={'text-align':'center'}),
                                       html.Th("2nd quartile", style={'text-align':'center'}), 
                                       html.Th("3rd quartile", style={'text-align':'center'}),
                                       html.Th("Maximum", style={'text-align':'center'})]))]
    
        if actuators_table:
            actuators_table_header = [html.Thead(html.Tr([html.Th(""), 
                                       html.Th("Time slot", style={'text-align':'center'}),
                                       html.Th("Total time (h)", style={'text-align':'center'}), 
                                       html.Th("Energy (Wh)", style={'text-align':'center'}),
                                       html.Th("Cost (€)", style={'text-align':'center'})]))]
            
        graph = dcc.Graph(figure=figure)
        
        return [graph, sensors_table_header + sensors_table, actuators_table_header + actuators_table]
        
        
        