//
// Make a single stepper bounce from one limit to another
//

/*
  Instructions:
  - At least one of: (comment the appropriate code below)
      PW is digital pin 11
      TX is digital pin 6
      AN is analog pin A0
  - Change code below according to your model (LV, XL and
  HRLV supported)

  Note:
  For convenience, the getRange method will always return centimeters.
  You can use convert fuctions to convert to another unit (toInches and
  toCentimeters are available)

*/


// SERIAL commands
// Notes: B, G , D, E (also b2 but not real note)
// ALL - A
// Numbers - position on the wheel

//1600 steps

#include <AccelStepper.h>
// Define a stepper and the pins it will use
AccelStepper stepper(AccelStepper::FULL2WIRE, 9, 8);

// ****** SPEEDS ******
int multiplier = 1800; // WAS 2000
int regSpeed = multiplier * 4;
int regAcc = multiplier * 6;
int fastSpeed = multiplier * 5;
int fastAcc = multiplier * 6;
int slowSpeed = multiplier * 2;
int slo2Acc = multiplier * 4;


// ****** VARIABLES ******
int hot = 0;
int noteCount = 0;
String last = "0";
int barCount = 8;




//timing
unsigned long interval = 4000; // the time we need to wait
unsigned long interval2 = 1000; // the time we need to wait

unsigned long previousMillis = 0; // millis() returns an unsigned long.
unsigned long previousMillisNote = 0; // millis() returns an unsigned long.
unsigned long currentMillis = 0; // millis() returns an unsigned long.




// String input
String inputString = "";         // a string to hold incoming data
boolean stringComplete = false;  // whether the string is complete
String cmd = "";

// *************** END OF PARAMS *******************


// *************** Read Serial Events ***************
void serialEvent() {
  while (Serial.available()) {
    // get the new byte:
    char inChar = (char)Serial.read();
    // add it to the inputString:
    inputString += inChar;
    // if the incoming character is a newline, set a flag
    // so the main loop can do something about it:
    if (inChar == '\n') {
      stringComplete = true;
      //Serial.println(inputString);
      inputString.toLowerCase();
      cmd = inputString;




    }
  }

}

// *************** NOTE FUNCTIONS ***************

void playAll() {

  stepper.moveTo(4000);
  while (stepper.currentPosition() != 3800)  {
    stepper.setSpeed(regSpeed);
    stepper.runSpeedToPosition();
  }
  stepper.moveTo(0);
  while (stepper.currentPosition() != 200) {
    stepper.setSpeed(regSpeed);
    stepper.runSpeedToPosition();
  }
  noteCount = 0;
  cmd = last;

}

void playFull() {
  stepper.moveTo(7300);
  while (stepper.currentPosition() != 7000)  {
    stepper.setSpeed(regSpeed);
    stepper.runSpeedToPosition();
  }
  stepper.moveTo(0);
  while (stepper.currentPosition() != 0) {
    stepper.setSpeed(regSpeed);
    stepper.runSpeedToPosition();
  }
  if (stepper.distanceToGo() == 0) {
    stepper.setCurrentPosition(0);
  }
  noteCount = 0;
  cmd = last;
}


// ********** INDIVIDUAL NOTES *********** 


void playE1() {
  if (cmd != "e1\n") {
    return;
  } else if (noteCount >= barCount) {
    playAll();
    return;
  } else {
    stepper.moveTo(1500);
    while (stepper.currentPosition() != 1300)  {
      stepper.setSpeed(regSpeed);
      stepper.runSpeedToPosition();
    }
    stepper.moveTo(100);
    while (stepper.currentPosition() != 100) {
      stepper.setSpeed(regSpeed);
      stepper.runSpeedToPosition();
    }
    noteCount++;
    //      Serial.print("noteCount: ");
    //      Serial.println(noteCount);
  }
}


void playB() {
  if (cmd != "b\n") {
    return;
  } else if (noteCount >= barCount) {
    playAll();
    return;
  } else {
    stepper.moveTo(1900);
    while (stepper.currentPosition() != 1800)  {
      stepper.setSpeed(regSpeed);
      stepper.runSpeedToPosition();
    }
    stepper.moveTo(500);
    while (stepper.currentPosition() != 500) {
      stepper.setSpeed(regSpeed);
      stepper.runSpeedToPosition();
    }
    noteCount++;
    //      Serial.print("noteCount: ");
    //      Serial.println(noteCount);
  }
}

void playB2() {
  //    Serial.println("playing B2");
  if (cmd != "b2\n") {
    return;
  } else if (noteCount >= barCount) {
    playAll();
    return;
  } else {
    stepper.moveTo(1900);
    while (stepper.currentPosition() != 1800)  {
      stepper.setSpeed(regSpeed);
      stepper.runSpeedToPosition();
    }
    stepper.moveTo(500);
    while (stepper.currentPosition() != 500) {
      stepper.setSpeed(regSpeed);
      stepper.runSpeedToPosition();
    }
    noteCount++;
    //      Serial.print("noteCount: ");
    //      Serial.println(noteCount);
  }
}


void playG() {
  //  Serial.println("");
  if (cmd != "g\n") {
    return;
  } else if (noteCount >= barCount) {
    playAll();
    return;
  } else {
    stepper.moveTo(2400);
    while (stepper.currentPosition() != 2200)  {
      stepper.setSpeed(regSpeed);
      stepper.runSpeedToPosition();
    }
    stepper.moveTo(1000);
    while (stepper.currentPosition() != 1100) {
      stepper.setSpeed(regSpeed);
      stepper.runSpeedToPosition();
    }
    noteCount++;

  }
}

void playD() {
  //  Serial.println("");
  if (cmd != "d\n") {
    return;
  } else if (noteCount >= barCount) {
    playAll();
    return;
  } else {
    stepper.moveTo(2600);
    while (stepper.currentPosition() != 2500)  {
      stepper.setSpeed(regSpeed);
      stepper.runSpeedToPosition();
    }
    stepper.moveTo(1300);
    while (stepper.currentPosition() != 1500) {
      stepper.setSpeed(regSpeed);
      stepper.runSpeedToPosition();
    }
    noteCount++;

  }
}

void playA() {
  //  Serial.println("");
  if (cmd != "a\n") {
    return;
  } else if (noteCount >= barCount) {
    playAll();
    return;
  } else {
    stepper.moveTo(3000);
    while (stepper.currentPosition() != 2800)  {
      stepper.setSpeed(regSpeed);
      stepper.runSpeedToPosition();
    }
    stepper.moveTo(2000);
    while (stepper.currentPosition() != 2100) {
      stepper.setSpeed(regSpeed);
      stepper.runSpeedToPosition();
    }
    noteCount++;

  }
}

void playE() {
  //  Serial.println("");
  if (cmd != "e\n") {
    return;
  } else if (noteCount >= barCount) {
    playAll();
    return;
  } else {
    stepper.moveTo(3500);
    while (stepper.currentPosition() != 3500)  {
      stepper.setSpeed(regSpeed);
      stepper.runSpeedToPosition();
    }
    stepper.moveTo(2100);
    while (stepper.currentPosition() != 2200) {
      stepper.setSpeed(regSpeed);
      stepper.runSpeedToPosition();
    }
    noteCount++;

  }
}



// *************** SET SPEEDS ***************

void setSpeed (String value) {
  if (value == "regular") {
    //    Serial.println("Speed is regular");
    stepper.setMaxSpeed(regSpeed); //8000 seems to be a good speed
    stepper.setSpeed(regSpeed);
    stepper.setAcceleration(regAcc); // 18000 is a good number. Acceleration should be faster than speed for dick harp
  }
  if (value == "fast") {
    //        Serial.println("Speed is fast");
    //    stepper.setMaxSpeed(fastSpeed); //8000 seems to be a good speed
    stepper.setAcceleration(fastAcc); // 18000 is a good number. Acceleration should be faster than speed for dick harp
  }

  if (value == "slow") {
    //        Serial.println("Speed is slower");
    //    stepper.setMaxSpeed(slowSpeed); //8000 seems to be a good speed
    stepper.setSpeed(slowSpeed); //8000 seems to be a good speed
    //    stepper.setAcceleration(slowAcc); // 18000 is a good number. Acceleration should be faster than speed for dick harp
  }
}


// *************** SETUP ***************

void setup()
{

  //This opens up a serial connection to shoot the results back to the PC console
  Serial.begin(250000);
  // Change these to suit your stepper if you want
  setSpeed("regular");
  stepper.setSpeed(regSpeed);
  //  stepper.direction(CW);
  stepper.moveTo(0);

  inputString.reserve(200);

}

// *************** LOOP ***************

void loop() {
  unsigned long currentMillis = millis(); //grab current time
  if ((unsigned long)(currentMillis - previousMillis) >= interval) {


    // save the "current" time
    previousMillis = millis();

  }






  // *************** Loop Notes ***************
  if (cmd == "e1\n") {
    playE1();
  } else if (cmd == "b\n") {
    playB();
  } else if (cmd == "b2\n") {
    playB2();
  } else if (cmd == "g\n") {
    playG();
  } else if (cmd == "d\n") {
    playD();
  } else if (cmd == "e\n") {
    playE();
  } else if (cmd == "a\n") {
    playA();
  } else if (cmd == "l\n") {
    playAll();
  } else if (cmd == "f\n") {
    playFull();
  } else {
    hot = cmd.toInt();
    stepper.moveTo(hot);
    stepper.setSpeed(regSpeed);
    stepper.runSpeedToPosition();

  }


  // print the string when a newline arrives:
  if (stringComplete) {
    Serial.println(inputString);
    // clear the string:
    inputString = "";
    stringComplete = false;
  }
}

// *************** END OF LOOP ***************

