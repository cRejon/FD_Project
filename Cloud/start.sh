#! /bin/bash
sudo python3 /home/pi/App/MQTT_client.py $1 &
mod_wsgi-express start-server /home/pi/App/index.wsgi

