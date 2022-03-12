import paho.mqtt.subscribe as subscribe
import paho.mqtt.publish as publish

import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State


app = dash.Dash(__name__)
server = app.server
app.config.suppress_callback_exceptions = True


app.index_string = '''
<!DOCTYPE html>
<html>
    <head>
        {%metas%}
        <title>Plataforma IoT</title>
        {%favicon%}
        {%css%}
    </head>
    <body>
        {%app_entry%}
        <footer>
            {%config%}
            {%scripts%}            
            {%renderer%}
        </footer>
    </body>
</html>
'''