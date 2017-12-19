#!/usr/bin/env python

"""servoclass.py: connects to usbport and defines the movement of servo motors"""

import serial, glob


### assign arduino's serial port
try:
    portmotor = glob.glob("/dev/arduino-motors")[0]
except IndexError:
    portmotor = glob.glob("/dev/tty*")[0]
# portled = glob.glob("/dev/tty*")[0]
print("portmotor:", portmotor)
### set up serial baud rate
sermotor = serial.Serial(portmotor, 9600, timeout=1)
# serled = serial.Serial(portled, 9600, timeout=1)

class Servo:
    def __init__(self, servoID):
        self.servoID = servoID
        self.stop() # when initiated, stop!

    def move(self, speed):
        self.speed = speed
        if 0 <= self.speed <= 180:
            sermotor.write(chr(255))
            sermotor.write(chr(self.servoID))
            sermotor.write(chr(self.speed))
        else:
            print("Servo position must be an integer between 0 and 180.\n")

    def stop(self):
        self.move(90)
        #print("stop (90)")
