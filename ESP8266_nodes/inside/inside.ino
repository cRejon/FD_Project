#include <ESP8266WiFi.h>
#include <PubSubClient.h>
#include <ArduinoJson.h>
#include <DHT.h>


#define DHT_PIN D4
#define SOIL_PIN A0


// WiFi and MQTT broker configuration
const char* ssid = "WiFi-PFG";
const char* password = "********";
const char* mqtt_server = "192.168.4.1"; // Static IP address for RPi

DHT dht(DHT_PIN, DHT22);

WiFiClient espClient;
PubSubClient client(espClient);

float inTemp = 0.0;
int inHum = 0;
int soilHum = 0;
long rssi; // in dBm


void setup() { 
  
  Serial.begin(9600);

  config_wifi();
  client.setServer(mqtt_server, 1883);
  
  dht.begin();
}

void config_wifi() {
  delay(10);
  WiFi.mode(WIFI_STA);
  WiFi.begin(ssid, password);

  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
  }

}


void sendMQTT(){
  rssi = WiFi.RSSI() ;

  StaticJsonDocument<125> msg;
  msg["id"] = "inside";
  msg["signal"]= rssi;
  JsonObject measurements  = msg.createNestedObject("measurements");

  measurements["inTemp"] = inTemp;
  measurements["inHum"] = inHum;
  measurements["soilHum"] = soilHum;
  
  char JSONmsgBuffer[125];
  serializeJson(msg,JSONmsgBuffer);

  client.publish("greenhouse1/estate/inside", JSONmsgBuffer, true);// (topic, payload, retained)

}


void reconnect() {
  while (!client.connected()) {
    if (client.connect("inside", "greenhouse1/estate/inside", 2, true, "{\"id\":\"inside\",\"signal\":\"disconnected\"}")) {
      ;
    } else {
      delay(5000);
    }
  }
}


int readSoilHumidity()
{
    int readedValue;
    float percent;
    // slope and ordered at the origin calculated for this sensor
    float slope = -0.25;
    int orderedOrigin = 219;
    readedValue = analogRead(SOIL_PIN);
    percent= (slope*readedValue)+orderedOrigin; 
    if(percent<0){
    percent=0;
    }
    if(percent>100){
    percent=100;
    }
    return percent;
}



void loop() {

  if (!client.connected()) {
    reconnect();
  }
  client.loop();
  delay(2000);
  while (isnan(dht.readTemperature()) == 1) {
    delay(1000);
  }
  float inTempNow = dht.readTemperature();
  int inHumNow = int(dht.readHumidity());
  int soilHumNow = readSoilHumidity();


  bool cond1 = inTempNow <= (inTemp-0.5) || inTempNow >= (inTemp+0.5);
  bool cond2 = inHumNow <= (inHum-2) || inHumNow >= (inHum+2);
  bool cond3 = soilHumNow <= (soilHum-4) || soilHumNow >= (soilHum+4);

  if (cond1 || cond2 || cond3) {
    inTemp = inTempNow;
    inHum = inHumNow;
    soilHum = soilHumNow;

    sendMQTT();
  }
}
