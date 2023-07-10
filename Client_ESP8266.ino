#include <ESP8266WiFi.h>
#include <WiFiClient.h>
#include <ArduinoJson.h>
#include <EEPROM.h>

// Config eeprom and pin
const int buttonPin = 5;
const int eepromAddress = 0;
const int maxIpAddressLength = 16; // Maximum length of IP address string (including null terminator)

// Package's parameters
#define JSON_SIZE 512
#define PACK_SIZE 512

// WiFi credentials
const char* WIFI_SSID = "DESKTOP-JOHBFV1 4006";
const char* WIFI_PASSWORD = "12345678";
// const char* WIFI_SSID = "iPhone";
// const char* WIFI_PASSWORD = "123456789";

// IP address and port of the server
char* SERVER_IP;  // Replace with the server's IP address
const uint16_t SERVER_PORT = 8000;  // Replace with the server's port number

// Mock data values
DynamicJsonDocument pack(JSON_SIZE);
int16_t channel1 = 1, channel2 = 2, channel3 = 3, channel4 = 4, channel5 = 5, channel6 = 6, channel7 = 7, channel8 = 8, channel9 = 9, channel10 = 10, channel11 = 11, channel12 = 12, channel13 = 13, channel14 = 14, channel15 = 15, channel16 = 16;

// String
String json_string; 

// Header 8 bits
uint8_t header_Byte = 0;

WiFiClient client;

bool validateIPAddress(const String& ipAddress) {
  int count = 0;
  int dotCount = 0;
  for (size_t i = 0; i < ipAddress.length(); i++) {
    char c = ipAddress.charAt(i);
    if (c == '.') {
      dotCount++;
      if (count > 0 && count <= 255 && dotCount <= 3) {
        count = 0;
        continue;
      }
    }
    if (c >= '0' && c <= '9') {
      count = count * 10 + (c - '0');
    } else {
      return false; // Invalid character found
    }
  }
  return count > 0 && count <= 255 && dotCount == 3;
}

void read_IPaddress(){
  Serial.println("Enter IP address:");
  while (!Serial.available()) {
    // Wait until input is received
  }

  String ipAddress = Serial.readStringUntil('\n');
  ipAddress.trim();

  if (validateIPAddress(ipAddress)) {
    // IP address is valid, save it to EEPROM
    char savedIP[maxIpAddressLength];
    ipAddress.toCharArray(savedIP, maxIpAddressLength);
    EEPROM.put(eepromAddress, savedIP);
    EEPROM.commit();
    Serial.print("IP address saved to EEPROM: ");
    Serial.println(savedIP);
  } else {
    Serial.println("Invalid IP address!");
  }
}

void setup() {
  Serial.begin(115200);
  pinMode(buttonPin, INPUT);
  EEPROM.begin(512); // Initialize EEPROM library

  // Connect to Wi-Fi
  WiFi.begin(WIFI_SSID, WIFI_PASSWORD);
  while (WiFi.status() != WL_CONNECTED) {
    delay(1000);
    Serial.println("Connecting to WiFi...");
  }
  Serial.println("Connected to WiFi");

  // Check if IP address is saved in EEPROM
  char savedIP[maxIpAddressLength];
  EEPROM.get(eepromAddress, savedIP);
  if (savedIP[0] != '\0') {
    Serial.print("Saved IP Address: ");
    Serial.println(savedIP);
    SERVER_IP = savedIP;
    Serial.print("Current IP Address: ");
    Serial.println(savedIP);
    delay(1000);

    while(!client.connect(SERVER_IP, SERVER_PORT)){
      Serial.println("Failed to connect to server");
      delay(500);
      if (digitalRead(buttonPin) == HIGH) {
        read_IPaddress();
      }
    }
    Serial.println("Connected to server");
  }
}

void loop() {
  // IP input loop
  if (digitalRead(buttonPin) == HIGH) {
    read_IPaddress();
  }

  // Serialize the JSON-formated String
  pack["Channel1"] = String(channel1);
  pack["Channel2"] = String(channel2);
  pack["Channel3"] = String(channel3);
  pack["Channel4"] = String(channel4);
  pack["Channel5"] = String(channel5);
  pack["Channel6"] = String(channel6);
  pack["Channel7"] = String(channel7);
  pack["Channel8"] = String(channel8);
  pack["Channel9"] = String(channel9);
  pack["Channel10"] = String(channel10);
  pack["Channel11"] = String(channel11);
  pack["Channel12"] = String(channel12);
  pack["Channel13"] = String(channel13);
  pack["Channel14"] = String(channel14);
  pack["Channel15"] = String(channel15);
  pack["Channel16"] = String(channel16);
  serializeJson(pack, json_string);

  if (header_Byte >= 8){
    header_Byte -= 8;
  }

  // Constructing the package
  String package_string = String(header_Byte) + json_string;
  while(package_string.length() < PACK_SIZE){
    package_string += "|";
  }

  unsigned long startTime = millis();

  // while (millis() - startTime <= 5000) {
  while (1) {
    // Send the message
    client.print(package_string);
    Serial.println("Message sent");
    Serial.println("Header num: " + String(header_Byte) + ", " + "JSON size: " + String(json_string.length()) + ", " + "Package size: " + String(package_string.length()));

    String response = client.readStringUntil('\n');
    delay(200);
    if (response.startsWith(String(header_Byte))) {
      // ackReceived = true;
      Serial.println("ACK received");
      break;
    }

    else{
      // Serial.println("Timeout: ACK not received");
      // Resend the message
      client.println(package_string);
      Serial.println("Message resent");
      Serial.println("Header num: " + String(header_Byte) + ", " + "JSON size: " + String(json_string.length()) + ", " + "Package size: " + String(package_string.length()));
    } 
  }  
  json_string = "";
  header_Byte += 1;
}
