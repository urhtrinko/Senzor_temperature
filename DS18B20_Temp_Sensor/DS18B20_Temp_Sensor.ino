/* Arduino DS18B20 temp sensor tutorial
   More info: http://www.ardumotive.com/how-to-use-the-ds18b20-temperature-sensor-en.html
   Date: 19/6/2015 // www.ardumotive.com */

//Include libraries
#include <OneWire.h>
#include <DallasTemperature.h>
#define STOP_COMMAND "STOP"  // Command to stop execution

// Data wire is plugged into pin 2 on the Arduino
#define ONE_WIRE_BUS 2
// Setup a oneWire instance to communicate with any OneWire devices (not just Maxim/Dallas temperature ICs)
OneWire oneWire(ONE_WIRE_BUS);
// Pass our oneWire reference to Dallas Temperature. 
DallasTemperature sensors(&oneWire);

// Precisely timed output
unsigned long previousMillis = 0;  // Store the last time measurement was printed
const long interval = 1000;        // Interval to wait (1 second)

void setup(void)
{
  Serial.begin(9600); //Begin serial communication
  Serial.println("Arduino Digital Temperature // Serial Monitor Version"); //Print a message
  sensors.begin();
}

void loop(void)
{
  unsigned long currentMillis = millis();  // Get the current time
  // measure precisely every second
  if (currentMillis - previousMillis >= interval) {
    // Save the last time a measurement was printed
    previousMillis = currentMillis;
    // Send the command to get temperatures
    sensors.requestTemperatures();  
    Serial.print("Temperatura je: ");
    Serial.print(sensors.getTempCByIndex(0)); // Why "byIndex"? You can have more than one IC on the same bus. 0 refers to the first IC on the wire
    Serial.print("\xC2\xB0"); // add degree celcius symbol
    Serial.println("C");
  }

  // Stop code execution when th STOP command is written in the serial monitor
  if (Serial.available() > 0) {
    String command = Serial.readStringUntil('\n');  // Read the command until newline
    command.trim();  // Remove any leading/trailing whitespace

    // Check if the command matches STOP_COMMAND
    if (command == STOP_COMMAND) {
      // Action to stop or interrupt execution
      Serial.println("Konec merjenja temperature.");
      while (true) {
        // Infinite loop to stop further execution
      }
    }
  }  
}