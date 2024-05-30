#include <ArduinoMqttClient.h>
#include <WiFi.h> // For ESP32

// Define your WiFi credentials here
const char* ssid = "CS_Class";        // replace with your WiFi SSID
const char* password = "26430686";    // replace with your WiFi password

WiFiClient wifiClient;
MqttClient mqttClient(wifiClient);

const char broker[] = "highway.us.to";
int        port     = 1883;
const char topic[]  = "tofu/road";

void setup() {
  // Initialize serial and wait for port to open:
  Serial.begin(115200);
  while (!Serial) {
    ; // wait for serial port to connect. Needed for native USB port only
  }
  pinMode(23, OUTPUT);
  pinMode(22, OUTPUT);
  pinMode(21, OUTPUT);
  
  // Attempt to connect to WiFi network:
  Serial.print("Connecting to ");
  Serial.println(ssid);

  WiFi.begin(ssid, password);

  // Wait until the device is connected to WiFi
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }
  
  // When connected, print the IP address
  Serial.println("");
  Serial.println("WiFi connected");
  Serial.println("IP address: ");
  Serial.println(WiFi.localIP());

  // Attempt to connect to the MQTT broker
  Serial.print("Attempting to connect to the MQTT broker: ");
  Serial.println(broker);

  if (!mqttClient.connect(broker, port)) {
    Serial.print("MQTT connection failed! Error code = ");
    Serial.println(mqttClient.connectError());

    while (1);
  }

  Serial.println("You're connected to the MQTT broker!");
  Serial.println();

  Serial.print("Subscribing to topic: ");
  Serial.println(topic);
  Serial.println();

  // Subscribe to a topic
  mqttClient.subscribe(topic);

  Serial.print("Waiting for messages on topic: ");
  Serial.println(topic);
  Serial.println();
}

void loop() {
  int messageSize = mqttClient.parseMessage();
  if (messageSize) {
    // We received a message, print out the topic and contents
    Serial.print("Received a message with topic '");
    Serial.print(mqttClient.messageTopic());
    Serial.print("', length ");
    Serial.print(messageSize);
    Serial.println(" bytes:");

    // Use the Stream interface to print the contents
    String messageContent = "";
    while (mqttClient.available()) {
      char c = mqttClient.read();
      messageContent += c;
      Serial.print(c);
    }
    Serial.println();
    Serial.println();
    digitalWrite(23,LOW);
    digitalWrite(22,LOW);
    digitalWrite(21,LOW);
    // Control LED based on message content
    if (messageContent.equals("north")) {
      digitalWrite(23, HIGH); // Turn on north LED
    } else if (messageContent.equals("middle")) {
      digitalWrite(22, HIGH); // Turn on middle LED
    } else if (messageContent.equals("south")) {
      digitalWrite(21, HIGH); // Turn on south LED
    }
  }
}
