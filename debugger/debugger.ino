#define OUT_MODE (0x80)
#define IN_MODE  (0x40)
#define ANALOG_MODE (0x20)
#define DIGITAL_MODE (0x10)

void setup() {
  // put your setup code here, to run once:
  Serial.begin(9600);
}

void handleCommand(byte command[])
{
  /*Serial.println(command[0]);
  Serial.println(command[1]);
  Serial.println(command[2]);
  Serial.println(command[3]);*/
  if (command[0] & OUT_MODE) {
    Serial.println("out");
    //extract pin and value
    int pin_num = (int) command[1];
    int value_num = (int) command[2];
    value_num = (value_num << 8) + (int)command[3];
    Serial.print("value_num = ");
    Serial.println(value_num);
    pinMode(pin_num, OUTPUT);
    if (command[0] & DIGITAL_MODE) {
      Serial.println("digital write");
      digitalWrite(pin_num, value_num);
    }
    else if (command[0] & ANALOG_MODE) {
      Serial.println("analog write");
      analogWrite(pin_num, value_num);
    }
  }
  else if (command[0] & IN_MODE) {
    Serial.println("in");
    int pin_num = (int) command[1];
    int result = 0;
    pinMode(pin_num, INPUT);
    if (command[0] & DIGITAL_MODE) {
      result = digitalRead(pin_num);
    }
    else if (command[0] & ANALOG_MODE) {
      result = analogRead(pin_num);
    }
    Serial.print("read: ");
    Serial.println(result);
  }
}

void loop() {
  // put your main code here, to run repeatedly:
   if (Serial.available() > 0) {

    byte command[4] = {0};
    Serial.readBytes(command, 4);
    handleCommand(command);
  }
}
