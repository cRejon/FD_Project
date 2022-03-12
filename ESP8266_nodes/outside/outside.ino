
#include <ESP8266WiFi.h>
#include <PubSubClient.h>
#include <ArduinoJson.h>
#include <DHT.h>

#define DHT_PIN D4
#define DOOR_PIN D0 
#define DOOR_POWER D2


// WiFi and MQTT broker configuration
const char* ssid = "WiFi-PFG";
const char* password = "********";
const char* mqtt_server = "192.168.4.1";  // Static IP address for RPi

DHT dht(DHT_PIN, DHT22);

WiFiClient espClient;
PubSubClient client(espClient);

float outTemp = 0.0 ;
int outHum = 0;
int door = 0; 
long rssi; // in dBm


void setup() {
  pinMode(DOOR_PIN, INPUT);
  pinMode(DOOR_POWER, OUTPUT);
  digitalWrite(DOOR_POWER, LOW);
 
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
  msg["id"] = "outside";
  msg["signal"]= rssi;
  JsonObject measurements  = msg.createNestedObject("values");
  
  measurements["outTemp"] = outTemp;
  measurements["outHum"] = outHum;
  measurements["door"] = door;

  char JSONmsgBuffer[125];
  serializeJson(msg,JSONmsgBuffer);

  client.publish("greenhouse1/estate/outside", JSONmsgBuffer, true); // (topic, payload, retained)

}


void reconnect() {
  while (!client.connected()) {
    if (client.connect("outside", "greenhouse1/estate/outside", 2, true, "{\"id\":\"outside\",\"signal\":\"disconnected\"}")) {
     ;
    } else {
      delay(5000);
    }
  }
}


int checkDoor()
{
    int open;
    digitalWrite(DOOR_POWER, HIGH);
    delay(20);
    if (digitalRead(DOOR_PIN)==LOW){
      open = 100;
    }
    else {
      open = 0;
    } 
    digitalWrite(DOOR_POWER, LOW);
    return open; 
}


void loop() {

  if (!client.connected()) {
    reconnect();
  }
  client.loop();

  delay(500);
  int doorNow = checkDoor();
  while (isnan(dht.readTemperature()) == 1) {
    delay(1000);
  }
  float outTempNow = dht.readTemperature();
  int outHumNow = int(dht.readHumidity());
  
  bool cond1 = (doorNow != door);
  bool cond2 = (outTempNow <= (outTemp-0.5) || outTempNow >= (outTemp+0.5));
  bool cond3 = (outHumNow <= (outHum-2) || outHumNow >= (outHum+2));

  if (cond1 || cond2 || cond3) {
    door = doorNow;
    outTemp = outTempNow;
    outHum = outHumNow;

    sendMQTT();
  }
}
