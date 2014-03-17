/* This program allows you to set DMX channels over the serial port.
**
** Set the baud rate to 115200. 
** The following buad rates work: 9600, 19200, 38400 and 11520
** The others don't sends any messages to DMX. 
** You can then set DMX channels using these commands:
**
** <number>c : Select DMX channel
** <number>v : Set DMX channel to new value
**
** These can be combined. For example:
** 100c355w : Set channel 100 to value 255.
**
** For more details, and compatible Processing sketch,
** visit http://code.google.com/p/tinkerit/wiki/SerialToDmx
**
** Help and support: http://groups.google.com/group/dmxsimple       */
 
#include <DmxSimple.h>
 
void setup() {
  Serial.begin(115200);
  Serial.println("SerialToDmx ready");
  Serial.println();
  Serial.println("Syntax:");
  Serial.println(" 123c : use DMX channel 123");
  Serial.println(" 45w  : set current channel to value 45");
 
    DmxSimple.usePin(4);
  pinMode(2,OUTPUT);
  digitalWrite(2,HIGH);
}
 
int value = 0;
int channel;
 
void loop() {
  int c;
 
  while(!Serial.available());
  c = Serial.read();
  if ((c>='0') && (c<='9')) {
    value = 10*value + c - '0';
  } else {
    if (c=='c') channel = value;
    else if (c=='w') {
      DmxSimple.write(channel, value);
      Serial.println();
    }
    value = 0;
  }
}
