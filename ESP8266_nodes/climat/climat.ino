#include <ESP8266WiFi.h>
#include <PubSubClient.h>
#include <ArduinoJson.h>

#define  VENTILATION_PIN D7
#define  HEATING_PIN D4
#define  REFRIGERATION_PIN D0


// WiFi and MQTT broker configuration
const char* ssid = "WiFi-PFG";
const char* password = "********";
const char* mqttServer = "192.168.4.1";  // Static IP address for RPi

WiFiClient espClient;
PubSubClient client(espClient);

long lastMsg = 0;
long rssi;
int ventilation = 0;
int heating = 0;
int refrigeration = 0;

void setup() {
  pinMode(VENTILATION_PIN, OUTPUT);
  digitalWrite(VENTILATION_PIN, HIGH);
  pinMode(HEATING_PIN, OUTPUT);
  digitalWrite(HEATING_PIN, HIGH);
  pinMode(REFRIGERATION_PIN, OUTPUT);
  digitalWrite(REFRIGERATION_PIN, HIGH);
  
  Serial.begin(9600);
  
  config_wifi();
  client.setServer(mqttServer, 1883);
  client.setCallback(callback);
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

  if (msg == "activate_ventilation"){
     digitalWrite(VENTILATION_PIN, LOW);
     ventilation = 100;
     heating = 0;
     refrigeration = 0;
  } 
  else if (msg == "activate_heating"){
     digitalWrite(HEATING_PIN, LOW);
     ventilation = 0;
     heating = 100;
     refrigeration = 0;
  }    
  else if (msg == "activate_refrigeration"){
     digitalWrite(REFRIGERATION_PIN, LOW);
     ventilation = 0;
     heating = 0;
     refrigeration = 100;
  }
  else {  // shutdown case or sending errors
     digitalWrite(VENTILATION_PIN, HIGH);
     digitalWrite(HEATING_PIN, HIGH);
     digitalWrite(REFRIGERATION_PIN, HIGH);
     ventilation = 0;
     heating = 0;
     refrigeration = 0;
 
  } 
  sendMQTT(); 
}

void sendMQTT(){
  rssi = WiFi.RSSI() ;

  StaticJsonDocument<125> msg;
  msg["id"] = "climat";
  msg["signal"]= rssi;
  JsonObject measurements  = msg.createNestedObject("values");
  measurements["ventilation"] = ventilation;
  measurements["heating"] = heating;
  measurements["refrigeration"] = refrigeration;

  char JSONmsgBuffer[125];
  serializeJson(msg,JSONmsgBuffer);
  
  client.publish("greenhouse1/estate/climat", JSONmsgBuffer, true); // (topic, payload, retained)
}


void reconnect() {
  while (!client.connected()) {
    Serial.print("Trying MQTT connection...");
    // if disconnected, it will subscribe to topics
    if (client.connect("climat", "greenhouse1/estate/climat", 2, true, "{\"id\":\"climat\",\"signal\":\"disconnected\"}")) {
      client.subscribe("greenhouse1/control/climat");
      sendMQTT();
    } else {
      delay(5000);
    }
  }
}


void loop() {

  if (!client.connected()) {
    reconnect();
  }
  client.loop();
}
