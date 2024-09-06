// pin (analog input, A0) na katerega je priklopljen senzor (vanj pošilja informacije)
// pomni analog da razpon vrednosti med 0 in 1023
#define sensorPin A0

void setup() {
  // komunikacija s serial monitorjem na baud rate 9600
  Serial.begin(9600);
}

void loop() {
  // preberemo informacijo iz senzorja, ševilka med 0 in 1023 
  int reading = analogRead(sensorPin);

  // številko prevedemo v napetost
  float voltage = reading * (5.0/1024.0); // množimo s 5.0 saj je senzor priklopljen na 5 voltno napetost, delimo s 1024.0 ker je toliko možnih vrednosti 
                                          // nujno mora biti 5.0 in 1024.0, drugače obravnava rezultat kot intiger in je vedno enako 0
  // nato napetost prevedemo v temperaturo
  float temperatureC = (voltage - 0.5) * 100; // odštejemo offset ter množimo s 100 da dobimo iz voltov stopnije celzija

  // poročanje temperature
  Serial.print("Tempeartura: ");
  Serial.print(temperatureC);
  Serial.print("\xC2\xB0"); // dodaj simbol za stopnije celzija
  Serial.println("C");

  delay(1000); // vsako sekundo narejena meritev
}

