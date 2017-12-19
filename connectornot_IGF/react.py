#!/usr/bin/env python

"""The main interaction computation file"""
'''
syntax is python2
runs with 4 motors (and 2 LED strips);
motors pull the strings to make more room for passage when people use more data
LED colour should be mapped to a person and preserved until session ends
positioning uses fingerprints
'''

import time, servoclass, sys, random # ledclass,
from urllib2 import urlopen
from scipy.interpolate import interp1d
### DATA
# [0] - phoneID ;
# [1] - timestamp ;
# [2] - bytes ;
# [3] - conversation ;
# [4] - sms ;
# [5] - signalstrength ;
# [6] - estimote
# [7] - fingerpting

servoList = [servoclass.Servo(i+1) for i in range(4)]

def breathing(m1,m2,m3,addSpeed,addSpeed2,duration): # if speed = 10
    #breathe in
    m1.move(addSpeed) #80
    m3.move(addSpeed) #80
    m2.move(addSpeed2) #85
    time.sleep(duration)
    # breathe out
    m1.move(90-addSpeed) #92
    m3.move(90-addSpeed) #92
    m2.move(90-addSpeed2) #92
    time.sleep(duration)

def valuecase(value,scaling):
    s = interp1d([scaling[0], scaling[1]],[85,10])
    t = interp1d([scaling[0], scaling[1]],[1.5,5])
    if value > scaling[1]:
        speed = 10
        sleeping_time = 5
    else:
        speed = int(s(value))
        sleeping_time = float(t(value))
    return [speed, sleeping_time]

# begin with an empty user list, then append each new user to it and assign colors
userdict={}
while True:
    try:
        datas = urlopen("http://kucjica.kucjica.org/androidtesting/arduino-get.php")
        line = datas.read()
        #print(line)
        user = line.split(b';')[0].decode("utf-8")
        print('user', user)
        # assign color to a user, or read from userdict
        ### calculate the movement:
        bajts = abs(int(line.split(b';')[2]))
        #print("bajts", bajts)
        bajtsLimit=[0, 100000]
        speedBajt, sleepBajt = valuecase(bajts, bajtsLimit)
        print("speed according to bytes(which are ", bajts, ")", speedBajt)
        conv = int(line.split(b';')[3])
        #print("conv", conv)
        convLimit=[0, 120]
        speedConv, sleepConv = valuecase(conv, convLimit)
        print("speed according to conversation", speedConv)
        sms = int(line.split(b';')[4])
        #print("sms", sms)
        smsLimit = [0, 5]
        speedSms, sleepSms = valuecase(sms, smsLimit)
        print("speed according to sms", speedSms)
        signals = int(line.split(b';')[5])
        speedFinal = int((speedBajt+speedConv+speedSms)/3)
        sleepFinal = (sleepBajt+sleepConv+sleepSms)/3
        print("speed final", speedFinal, "sleep final", sleepFinal)
        ## locate in space
        ### and react depending on the closest fingerprint
        # without localization, addSpeed and addSpeed2 arguments should be equal
        # with localization, addSpeed should be always bigger from addSpeed2, which is calculated in funciton of the first
        fingerprint = line.split(b';')[7].decode('utf-8').strip()
        print('fingerprint', fingerprint)
        if fingerprint == "0":
            print("you are not here")
            breathing(servoList[0], servoList[1], servoList[2], speedFinal, speedFinal, sleepFinal)
        elif fingerprint == "131": # ulaz
            print('you are at ULAZ')
            breathing(servoList[0], servoList[1], servoList[2], speedFinal, speedFinal-2, sleepFinal)
        elif fingerprint == "132": # izlaz
            print('you are at IZlAZ')
            breathing(servoList[1], servoList[0], servoList[2], speedFinal, speedFinal-2, sleepFinal)
        else:
            print("something weird")
            breathing(servoList[0], servoList[1], servoList[2], speedFinal, speedFinal, sleepFinal)
        time.sleep(2)
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

'''TODO
LEDs
'''
