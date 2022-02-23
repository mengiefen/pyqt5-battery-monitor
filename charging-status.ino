#define controlPin  A3
#define measurePin A0

bool chargingState = false;
int counter = 0;

void setup() {
  // put your setup code here, to run once:
  Serial.begin(9600);
  pinMode(controlPin, OUTPUT);
  //digitalWrite(controlPin,HIGH);
}

void loop() {
  // put your main code here, to run repeatedly:
  int reading = readVoltage();

  //512 ==> 14.38Volts ==> Battery charger will be cut-off at this volatge
  //444 ===>12.45Volts ==> The battery will be charged when it reaches this voltage
  //491 ==> 13.8Volts ==> The battery will be cuttof

//  if ( reading >= 428 && counter == 0 && reading < 488) {
//    digitalWrite(controlPin, HIGH);
//    chargingState = false;
//    //counter = counter + 1;
//    delay(5000);
//  }

  if (reading <= 428 && reading >= 100 && chargingState == false) {
    digitalWrite(controlPin, LOW);
    chargingState = true;
    delay(5000);
  }
  else if ( reading >= 488 ) {
    digitalWrite(controlPin, HIGH);// should be HIGH
    chargingState = false;
    delay(5000);
  }
  
  Serial.print((float(reading)/1023)*5.0/0.174);  
  Serial.print(" Volts ");
  Serial.println(String(chargingState));   
}


int readVoltage() {
  int accumulator = 0;
  int reading;
  for (int i = 0 ; i < 12; i++) {
    reading = analogRead(measurePin);
    accumulator += reading;
    delay(5000);
  }
  return (accumulator / 12);
}
