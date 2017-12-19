#!/usr/bin/env python

"""The main interaction computation file"""
'''
syntax is python3
runs with 4 motors and 2 LED strips;
motors pull the strings to make more room for passage when people use more data
LED colour should be mapped to a person and preserved until session ends
positioning uses fingerprints
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

servoList = [servoclass.Servo(i+1) for i in range(4)]

# reactions to different events
def reaction(m1, m2, m3, addSpeed, duration):
    # m1 is the strongest motor, determined by entrance position
    # m1 and m3 are motors in the same half of the station, on opposite sides
    m1.move(90-addSpeed)
    m2.move(int(addSpeed/4))
    m3.move(90-addSpeed+2)
    #ledclass.fadeInUser(led) led deleted from arrtibutes
    time.sleep(duration)
    m1.stop()
    m2.stop()
    m3.stop()

def breathing(m1,m2,m3,addSpeed,addSpeed2,duration): # if speed = 10
    #breathe in
    m1.move(90-addSpeed) #80
    m3.move(90-addSpeed) #80
    m2.move(90-addSpeed2) #85
    time.sleep(duration)
    # breathe out
    m1.move(90+int(addSpeed*0.4)) #92
    m3.move(90+int(addSpeed*0.4)) #92
    m2.move(90+int(addSpeed2*0.4)) #92
    time.sleep(int(duration*1.5))

def valuecase(value,valuelist):
    if 0 <= value <= valuelist[0]:
        addSpeed = 10 #release a little
        sleeping_time = 1
    elif valuelist[0] < value <= valuelist[1]:
        addSpeed = 20 #tighten a little
        sleeping_time = 2
    elif valuelist[1] < value <= valuelist[2]:
        addSpeed = 30 #tighten even faster
        sleeping_time = 2
    elif valuelist[2] < value <= valuelist[3]:
        addSpeed = 50 #tighten very fast
        sleeping_time = 4
    elif valuelist[3] < value:
        addSpeed = 90 #tighten very very fast
        sleeping_time = 4
    else:
        print("none of the above byte values")
        speed = 0 # servo down_very_fast
    return [addSpeed, sleeping_time]

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
        if user not in userdict.keys():
            userCOLOR = random.randint(0,255)
            userdict[user]=userCOLOR
        else:
            userCOLOR = userdict[user]
        ### calculate the movement:
        bajts = abs(int(line.split(b';')[2]))
        #print("bajts", bajts)
        bajtsLimit=[150, 7000, 10000, 30000]
        speedBajt, sleepBajt = valuecase(bajts, bajtsLimit)
        print("speed according to bytes(which are ", bajts, speedBajt)
        conv = int(line.split(b';')[3])
        #print("conv", conv)
        convLimit=[2, 10, 50, 120]
        speedConv, sleepConv = valuecase(conv, convLimit)
        print("speed according to conversation", speedConv)
        sms = int(line.split(b';')[4])
        #print("sms", sms)
        smsLimit = [1, 2, 3, 4]
        speedSms, sleepSms = valuecase(sms, smsLimit)
        print("speed according to sms", speedSms)
        signals = int(line.split(b';')[5])
        speedFinal = int((speedBajt+speedConv+speedSms)/3)
        sleepFinal = int((sleepBajt+sleepConv+sleepSms)/3)
        print("speed final", speedFinal, "\nsleep final", sleepFinal)
        ## locate in space
        ### and react depending on the closest estimote
        fingerprint = line.split(b';')[7].decode('utf-8').strip()
        print('fingerprint', fingerprint)
        if fingerprint == "0":
            print("you are not here")
            breathing(servoList[0], servoList[1], servoList[2], speedFinal, speedFinal, sleepFinal)
                #ledclass.fadeInRed(i)
        elif fingerprint == "131": # ulaz
            print('you are at ULAZ')
            breathing(servoList[0], servoList[1], servoList[2], speedFinal, speedFinal-2, sleepFinal)
        elif fingerprint == "132": # izlaz
            print('you are at IZlAZ')
            breathing(servoList[1], servoList[0], servoList[2], speedFinal, speedFinal-2, sleepFinal)
        else:
            print("something weird")
            #if SELENA not in UserDict, do the following only
            '''
            print('breating out')
            reaction(servoList[0], servoList[1], servoList[2],  95, 16)
            time.sleep(1)
            print('breating out')
            reaction(servoList[0], servoList[1], servoList[2],  76, 8)
            time.sleep(1)
            '''
        # without localization, addSpeed and addSpeed2 arguments should be equal
        #breating(servoList[0], servoList[1], servoList[2], speedFinal, speedFinal sleepFinal)
        # with localization, addSpeed should be always bigger from addSpeed2, which is calculated in funciton of
        #breating(servoList[0], servoList[1], servoList[2], speedFinal, speedFinal sleepFinal)
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
