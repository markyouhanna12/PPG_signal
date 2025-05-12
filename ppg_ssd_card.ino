#include <SD.h>
#include <SPI.h>

#define PPG_PIN 34
#define BUTTON_PIN 14
#define LED_PIN 2
#define SD_CS_PIN 5

const int SAMPLE_COUNT = 310;
int samples[SAMPLE_COUNT];

bool sdAvailable = false;

void setup() {
  Serial.begin(115200);

  pinMode(PPG_PIN, INPUT);
  pinMode(BUTTON_PIN, INPUT_PULLUP);
  pinMode(LED_PIN, OUTPUT);
  digitalWrite(LED_PIN, LOW);

  if (!SD.begin(SD_CS_PIN)) {
    Serial.println("SD card initialization failed!");
    digitalWrite(LED_PIN, HIGH);  // LED ON to indicate error
  } else {
    Serial.println("SD card initialized.");
    sdAvailable = true;
    digitalWrite(LED_PIN, LOW);   // LED OFF
  }

  Serial.println("Press the button to start recording...");
}

String getNextAvailableFilename() {
  for (int i = 1; i <= 999; i++) {
    String filename = "/ppg_" + String(i) + ".csv";
    if (!SD.exists(filename)) {
      return filename;
    }
  }
  return "";  // No available slot
}

void loop() {

  
  if (!sdAvailable) {
    if (SD.begin(SD_CS_PIN)) {
      Serial.println("SD card inserted!");
      sdAvailable = true;
      digitalWrite(LED_PIN, LOW);
    } else {
      digitalWrite(LED_PIN, HIGH);
    }
  }

  if (sdAvailable && digitalRead(BUTTON_PIN) == LOW) {
    Serial.println("Recording started...");
    delay(200); // debounce

    for (int i = 0; i < SAMPLE_COUNT; i++) {
      samples[i] = analogRead(PPG_PIN);
      delay(50);
    }

    String filename = getNextAvailableFilename();
    if (filename == "") {
      Serial.println("No available filename (ppg_001-999.csv used).");
      return;
    }

    File file = SD.open(filename, FILE_WRITE);
    if (file) {
      for (int i = 0; i < SAMPLE_COUNT; i++) {
        file.println(samples[i]);
      }
      file.close();
      Serial.print("Data saved to ");
      Serial.println(filename);

      digitalWrite(LED_PIN, HIGH);
      delay(2000);
      digitalWrite(LED_PIN, LOW);
    } else {
      Serial.println("Failed to open file for writing.");
    }

    while (digitalRead(BUTTON_PIN) == LOW);
    delay(500);
    Serial.println("Ready for next recording...");
  }
}
