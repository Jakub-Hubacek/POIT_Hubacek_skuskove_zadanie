#include <Wire.h>
#include <Adafruit_MPU6050.h>
#include <Adafruit_Sensor.h>
#include <DHT.h>

#define DHTPIN 4
#define DHTTYPE DHT22

DHT dht(DHTPIN, DHTTYPE);
Adafruit_MPU6050 mpu;

const int sampleInterval = 100;      // in ms
const int measurementTime = 60000;   // 1 minute in ms

void setup() {
  Serial.begin(115200);
  delay(1000);

  dht.begin();
  Serial.println("DHT22 initialized.");

  if (!mpu.begin()) {
    Serial.println("Failed to find MPU6050 chip");
    while (1) delay(10);
  }

  Serial.println("MPU6050 initialized.");
  mpu.setAccelerometerRange(MPU6050_RANGE_8_G);
  mpu.setGyroRange(MPU6050_RANGE_500_DEG);
  mpu.setFilterBandwidth(MPU6050_BAND_21_HZ);
}

void loop() {
  Serial.println("Starting 1-minute monitoring cycle...");

  float sumSquares = 0;
  int sampleCount = 0;

  unsigned long startTime = millis();

  // Sampling loop for 1 minute
  while (millis() - startTime < measurementTime) {
    sensors_event_t a, g, temp;
    mpu.getEvent(&a, &g, &temp);

    float totalAccel = sqrt(
      a.acceleration.x * a.acceleration.x +
      a.acceleration.y * a.acceleration.y +
      a.acceleration.z * a.acceleration.z
    );

    float netVibration = abs(totalAccel - 9.8);
    sumSquares += netVibration * netVibration;
    sampleCount++;

    delay(sampleInterval);
  }

  // Calculate RMS vibration
  float rmsVibration = sqrt(sumSquares / sampleCount);

  // Read temperature and humidity
  float temperature = dht.readTemperature();
  float humidity = dht.readHumidity();

  if (isnan(temperature) || isnan(humidity)) {
    Serial.println("Failed to read from DHT sensor!");
  } else {
    Serial.printf("Temperature: %.2f °C | Humidity: %.2f %%\n", temperature, humidity);
  }

  Serial.printf("1-minute RMS Vibration Level: %.3f m/s²\n\n", rmsVibration);

  delay(5000); // Optional delay before next measurement cycle
}
