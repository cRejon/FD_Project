#include <ESP8266WiFi.h>
#include <PubSubClient.h>
#include <ArduinoJson.h>
#include <OneWire.h> 
#include <DallasTemperature.h>

#define  PUMP_PIN D7
#define  BUS_TEMP_PIN D2


// WiFi and MQTT broker configuration
const char* ssid = "WiFi-PFG";
const char* password = "********";
const char* mqttServer = "192.168.4.1"; // Static IP address for RPi

WiFiClient espClient;
PubSubClient client(espClient);

OneWire oneWire(BUS_TEMP_PIN);  
DallasTemperature waterTempSensor(&oneWire);

float waterTemp = 0.0;
int pump = 0;
long rssi; // in dBm


void setup() {
  pinMode(PUMP_PIN, OUTPUT);
  digitalWrite(PUMP_PIN, HIGH);
  
  Serial.begin(9600);
  
  config_wifi();
  client.setServer(mqttServer, 1883);
  client.setCallback(callback);

  waterTempSensor.begin();
}


void config_wifi() {
  delay(10);
  WiFi.mode(WIFI_STA);
  WiFi.begin(ssid, password);

  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
  }

}


void callback(char* topic, byte* payload, unsigned int length) {
  String msg = "";
  for (int i = 0; i < length; i++) {
    msg.concat((char)payload[i]);
  }
  if (msg == "activate_pump") { 
     pump= 100;
     digitalWrite(PUMP_PIN, LOW);   
  } 
  else { // turn off pump 
    pump= 0;
    digitalWrite(PUMP_PIN, HIGH);  
  }
  sendMQTT();
}

void sendMQTT(){
  rssi = WiFi.RSSI() ;

  StaticJsonDocument<125> msg;
  msg["id"] = "deposit";
  msg["signal"]= rssi;
  JsonObject measurements  = msg.createNestedObject("measurements");
  measurements["waterTemp"] = waterTemp;
  measurements["pump"] = pump;

  char JSONmsgBuffer[125];
  serializeJson(msg,JSONmsgBuffer);
  
  client.publish("greenhouse1/estate/deposit", JSONmsgBuffer, true);// (topic, payload, retained)

}


void reconnect() {
  while (!client.connected()) {
    if (client.connect("deposit", "greenhouse1/estate/deposit", 2, true, "{\"id\":\"deposit\",\"signal\":\"disconnected\"}")) {
      client.subscribe("greenhouse1/control/deposit");
    } else {
      delay(5000);
    }
  }
}


float read_water_temp()
{   
   waterTempSensor.requestTemperatures();
   // as it is a communication bus it takes the value of the first IC in the wire
   return round(waterTempSensor.getTempCByIndex(0) * 10) / 10;// round to one decimal
}


void loop() {

  if (!client.connected()) {
    reconnect();
  }
  client.loop();
  delay(500);
  float waterTempNow = read_water_temp();

  if (waterTempNow <= (waterTemp-0.5) || waterTempNow >= (waterTemp+0.5)) {
    waterTemp = waterTempNow;

    sendMQTT();
  }
}
