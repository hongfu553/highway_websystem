#include <WiFi.h>
#include <WebServer.h>

const char* ssid = "Xiaomi_3G";
const char* password = "29180064";

WebServer server(80);

const int ledPin = 2;  // ESP32板載LED通常連接到GPIO2

void setup() {
  Serial.begin(115200);
  pinMode(ledPin, OUTPUT);
  pinMode(23,OUTPUT);
  
  WiFi.begin(ssid, password);
  while (WiFi.status() != WL_CONNECTED) {
    delay(1000);
    Serial.println("正在連接到WiFi...");
  }
  Serial.println("已連接到WiFi");
  Serial.print("IP地址: ");
  Serial.println(WiFi.localIP());

  server.on("/", handleRoot);
  server.on("/led/on", handleLedOn);
  server.on("/led/off", handleLedOff);

  server.begin();
  Serial.println("HTTP服務器已啟動");
}

void loop() {
  server.handleClient();
}

void handleRoot() {
  String html = "<html><body>";
  html += "<h1>ESP32 Web Server</h1>";
  html += "<p><a href='/led/on'><button>Open PC</button></a></p>";
  html += "<p><a href='/led/off'><button>關閉LED</button></a></p>";
  html += "</body></html>";
  server.send(200, "text/html", html);
}

void handleLedOn() {
  digitalWrite(ledPin, HIGH);
  digitalWrite(23,HIGH);
  delay(400);
  digitalWrite(23,LOW);
  server.sendHeader("Location", "/");
  server.send(303);
}

void handleLedOff() {
  digitalWrite(ledPin, LOW);
  server.sendHeader("Location", "/");
  server.send(303);
}