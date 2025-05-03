#include <WiFi.h>
#include <HTTPClient.h>
#include <ArduinoJson.h>
#include <DHT.h>
#include <time.h>
#include <FS.h>
#include <SPIFFS.h>

// ==== WiFi Credentials ====
const char* ssid = "ZTE-WIFI";
const char* password = "04072002";

// ==== API Info ====
const char* loginUrl = "http://192.168.1.142:8000/login";
const char* refreshUrl = "http://192.168.1.142:8000/refresh";
const char* tempUrl = "http://192.168.1.142:8000/temp/";
const char* humidityUrl = "http://192.168.1.142:8000/humidity/";
const char* coolingUrl = "http://192.168.1.142:8000/cooling/";
const char* coolingStatusUrl = "http://192.168.1.142:8000/cooling/status";

// ==== DHT Sensor ====
#define DHTPIN 4
#define DHTTYPE DHT22
DHT dht(DHTPIN, DHTTYPE);

// ==== Relay Pin ====
const int relayPin = 5;

// ==== Authentication Tokens ====
String accessToken = "";
String refreshToken = "";
unsigned long tokenObtainedTime = 0;
const unsigned long tokenValidity = 480 * 60 * 1000UL; // 480 minutes

// ==== Timer ====
unsigned long lastSent = 0;
const unsigned long sendInterval = 10000;

// ==== Login Credentials ====
String loginUser = "jakub";
String loginPass = "jakub";

// ==== Time Sync ====
const char* ntpServer = "pool.ntp.org";

// ==== File Buffers ====
const char* bufferFile = "/unsent.txt";
int getCoolingStatus();
int lastCoolingStatus = getCoolingStatus(); // Initialize to an invalid state
int coolingStatus = 0;
void setup() {
  Serial.begin(115200);
  dht.begin();
  pinMode(relayPin, OUTPUT);
  digitalWrite(relayPin, LOW);

  SPIFFS.begin(true);

  WiFi.begin(ssid, password);
  Serial.print("Connecting to WiFi");
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }
  Serial.println(" connected.");

  configTime(0, 0, ntpServer);
  while (time(nullptr) < 100000) delay(100); // wait for time sync

  if (!login()) {
    Serial.println("Initial login failed!");
  }
}

void loop() {
  
  if ((millis() - lastSent >= sendInterval)) {
    if (!isTokenValid()) {
      if (!refreshAccessToken()) {
        if (!login()) {
          Serial.println("Re-authentication failed.");
          return;
        }
      }
    }

    float temperature = dht.readTemperature();
    float humidity = dht.readHumidity();
    lastCoolingStatus = coolingStatus;
    coolingStatus = getCoolingStatus();

    bool cooling = coolingStatus == 1;
    if (!cooling && temperature > 55) {
      cooling = true;
    } 
    digitalWrite(relayPin, cooling ? HIGH : LOW);

    String timestamp = getISO8601Time();

    // Try sending any buffered data first
    resendBufferedData();

    // Send current data
    bool tempOk = sendSensorData(tempUrl, "temp", temperature, timestamp);
    bool humOk = sendSensorData(humidityUrl, "humidity", humidity, timestamp);
    bool coolOk = sendSensorData(coolingUrl, "cooling", cooling ? 1 : 0, timestamp);

    // If any failed, store it
    if (!tempOk) bufferData(tempUrl, "temp", temperature, timestamp);
    if (!humOk)  bufferData(humidityUrl, "humidity", humidity, timestamp);
    if (!coolOk) bufferData(coolingUrl, "cooling", cooling ? 1 : 0, timestamp);

    lastSent = millis();
  }
}

bool isTokenValid() {
  return millis() - tokenObtainedTime < tokenValidity;
}

bool login() {
  HTTPClient http;
  http.begin(loginUrl);
  http.addHeader("Content-Type", "application/x-www-form-urlencoded");

  String body = "grant_type=password"
                "&username=" + loginUser +
                "&password=" + loginPass +
                "&scope=" +
                "&client_id=string"
                "&client_secret=string";

  int httpCode = http.POST(body);

  if (httpCode == 200) {
    String payload = http.getString();
    DynamicJsonDocument doc(1024);
    deserializeJson(doc, payload);

    accessToken = doc["access_token"].as<String>();
    refreshToken = doc["refresh_token"].as<String>();
    tokenObtainedTime = millis();

    Serial.println("Login successful.");
    return true;
  } else {
    Serial.println("Login failed: " + String(httpCode));
    Serial.println(http.getString());
    return false;
  }
}


bool refreshAccessToken() {
  HTTPClient http;
  http.begin(refreshUrl);
  http.addHeader("Content-Type", "application/json");

  DynamicJsonDocument doc(256);
  doc["refresh_token"] = refreshToken;
  String body;
  serializeJson(doc, body);

  int httpCode = http.POST(body);
  if (httpCode == 200) {
    String payload = http.getString();
    deserializeJson(doc, payload);

    accessToken = doc["access_token"].as<String>();
    refreshToken = doc["refresh_token"].as<String>();
    tokenObtainedTime = millis();

    Serial.println("Token refreshed.");
    return true;
  } else {
    Serial.println("Token refresh failed: " + String(httpCode));
    return false;
  }
}

bool sendSensorData(const char* url, const char* key, float value, const String& timestamp) {
  if (WiFi.status() != WL_CONNECTED) {
    Serial.println("WiFi not connected.");
    return false;
  }

  HTTPClient http;
  http.begin(url);
  http.addHeader("Content-Type", "application/json");
  http.addHeader("Authorization", "Bearer " + accessToken);

  DynamicJsonDocument doc(256);
  doc[key] = value;
  doc["timestamp"] = timestamp;
  Serial.println("Sending data: " + String(key) + " = " + String(value));
  Serial.println("Timestamp: " + timestamp);
  String body;
  serializeJson(doc, body);

  int httpCode = http.POST(body);
  Serial.printf("POST to %s [%d]\n", url, httpCode);
  http.end();

  return httpCode >= 200 && httpCode < 300;
}

void bufferData(const char* url, const char* key, float value, const String& timestamp) {
  File file = SPIFFS.open(bufferFile, FILE_APPEND);
  if (!file) return;

  DynamicJsonDocument doc(256);
  doc["url"] = url;
  doc[key] = value;
  doc["timestamp"] = timestamp;

  String jsonStr;
  serializeJson(doc, jsonStr);
  file.println(jsonStr);
  file.close();

  Serial.println("Buffered unsent data.");
}

void resendBufferedData() {
  if (WiFi.status() != WL_CONNECTED || !SPIFFS.exists(bufferFile)) return;

  File file = SPIFFS.open(bufferFile, FILE_READ);
  if (!file) return;

  File tempFile = SPIFFS.open("/temp.txt", FILE_WRITE);
  if (!tempFile) return;

  while (file.available()) {
    String line = file.readStringUntil('\n');
    DynamicJsonDocument doc(256);
    DeserializationError err = deserializeJson(doc, line);

    if (err) continue;

    const char* url = doc["url"];
    String timestamp = doc["timestamp"];
    float value = doc["temp"] | doc["humidity"] | doc["cooling"];

    String key;
    if (doc.containsKey("temp")) key = "temp";
    else if (doc.containsKey("humidity")) key = "humidity";
    else if (doc.containsKey("cooling")) key = "cooling";

    if (!sendSensorData(url, key.c_str(), value, timestamp)) {
      tempFile.println(line);  // Still failed, keep in temp
    }
  }

  file.close();
  tempFile.close();

  SPIFFS.remove(bufferFile);
  SPIFFS.rename("/temp.txt", bufferFile);
}

String getISO8601Time() {
  time_t now;
  struct tm timeinfo;
  char buffer[30];

  time(&now);
  now += 2 * 3600; // Adjust for timezone (UTC+2)
  gmtime_r(&now, &timeinfo);
  strftime(buffer, sizeof(buffer), "%Y-%m-%dT%H:%M:%S.000Z", &timeinfo);
  return String(buffer);
}


int getCoolingStatus() {
  if (WiFi.status() != WL_CONNECTED) {
    Serial.println("WiFi not connected.");
    return -1; // Return -1 to indicate an error
  }

  HTTPClient http;
  http.begin(coolingStatusUrl);
  http.addHeader("Authorization", "Bearer " + accessToken);

  int httpCode = http.GET();
  if (httpCode == 200) {
    String payload = http.getString();
    http.end();
    return payload.toInt(); // Convert the response to an integer
  } else {
    Serial.println("Failed to get cooling status: " + String(httpCode));
    http.end();
    return -1; // Return -1 to indicate an error
  }
}