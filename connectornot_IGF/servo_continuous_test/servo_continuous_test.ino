// servo test 180 > 0 > 180

#include <Servo.h> 
 
Servo myservo1;  // create servo object to control a servo 
Servo myservo2;
Servo myservo3;
 
int val;    // variable to read the value from the analog pin 
 
void setup() 
{ 
  myservo1.attach(11,600,2100);  // attaches the servo on pin 12 to the servo object 
  myservo2.attach(12,600,2100);
  myservo3.attach(13,600,2100);
  Serial.begin(9600);
} 
 
void loop() 
{  
myservo1.write(120);
myservo2.write(120);
myservo3.write(120);

} 

