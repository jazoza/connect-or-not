#!/usr/bin/env python

"""The main interaction computation file / Iddle state"""
'''
syntax is python3
runs with 3 motors and 1 LED strip;
breathing movement
'''

import time, servoclass, sys, random # ledclass,
from urllib2 import urlopen
### DATA
# [0] - phoneID ;
# [1] - timestamp ;
# [2] - bytes ;
# [3] - conversation ;
# [4] - sms ;
# [5] - signalstrength ;
# [6] - estimote
# [7] - fingerpting

servoList = [servoclass.Servo(i+1) for i in range(3)]

# reactions to different events
def reaction(m1, m2, m3, speed, duration):
    # m1 is the strongest motor, determined by entrance position
    # m1 and m3 are motors in the same half of the station, on opposite sides
    m1.move(speed)
    m2.move(speed)
    m3.move(speed)
    #ledclass.fadeInUser(led) led deleted from arrtibutes
    time.sleep(duration)
    m1.stop()
    m2.stop()
    m3.stop()


# begin with an empty user list, then append each new user to it and assign colors

while True:
    try:
        print('breating in')
        reaction(servoList[0], servoList[1], servoList[2],  76, 8)
        time.sleep(1)
        print('breating out')
        reaction(servoList[0], servoList[1], servoList[2],  95, 16)
        time.sleep(1)
    except KeyboardInterrupt:
        for i in range(len(servoList)):
            servoList[i].move(90)
        sys.exit()
'''
### WORK FLOW:

### read in the db

### parse values; what has changed since last time
####### use timestamp?

### compute the reaction
### lights to represent bytes and conversation

### move things, lights
'''
