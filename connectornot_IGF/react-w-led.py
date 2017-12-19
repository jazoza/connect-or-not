#!/usr/bin/env python

"""The main interaction computation file"""

import urllib2, time, glob, serial
print glob.glob("/dev/ttyACM*")
portnumber = raw_input("wich port? ")
portled = glob.glob("/dev/ttyACM"+str(portnumber))[0]
serled = serial.Serial(portled, 19200, timeout=1)
print "portled:", portled

red = "255,0,0\n"
green = "0,0,255\n"
blue = "0,255,0\n"
yellow = "255,0,255\n"
purple = "255,255,0\n"
white = "255,255,255\n"
whitish = "100,100,100\n"
black = "0,0,0\n"


serled.write("0,"+purple)
serled.write("1,"+purple)
serled.write("2,"+purple)
serled.write("3,"+purple)
### DATA
### [0] - phoneID ; [1] - timestamp ; [2] - bytes ; [3] - conversation ; [4] - sms ; [5] - signalstrength ; [6] - estimote

# fading IN functions by colour:

def fadeInRed(led):
    for i in range(255)[::25]:
        message = (str(led)+",%d,0,0")%(i)
        serled.write(message+"\n")

def fadeInGreen(led):
    for i in range(255)[::25]:
        message = (str(led)+",0,0,%d")%(i)
        serled.write(message+"\n")

def fadeInYellow(led):
    for i in range(255)[::25]:
        message = (str(led)+",%d,0,%d")%(i,i)
        serled.write(message+"\n")

def fadeInPurple(led):
    for i in range(255)[::15]:
        message = (str(led)+",%d,%d,0")%(i,int(i*0.2))
        serled.write(message+"\n")

def fadeInTurq(led):
    for i in range(255)[::15]:
        message = (str(led)+",0,%d,%d")%(int(i*0.2),i)
        serled.write(message+"\n")

# fading OUT functions by colour:

def fadeOutRed(led):
    for i in range(255,0,-1)[::25]:
        message = (str(led)+",%d,0,0")%(i)
        serled.write(message+"\n")
        serled.write(str(led)+",0,0,0\n")

def fadeOutGreen(led):
    for i in range(255,0,-1)[::25]:
        message = (str(led)+",0,0,%d")%(i)
        serled.write(message+"\n")
        serled.write(str(led)+",0,0,0\n")
def fadeOutYellow(led):
    for i in range(255,0,-1)[::25]:
        message = (str(led)+",%d,0,%d")%(i,i)
        serled.write(message+"\n")
        serled.write(str(led)+",0,0,0\n")

def fadeOutPurple(led):
    for i in range(255,0,-1)[::25]:
        message = (str(led)+",%d,%d,0")%(i,int(i*0.2))
        serled.write(message+"\n")
        serled.write(str(led)+",0,0,0\n")

def fadeOutTurq(led):
    for i in range(255,0,-1)[::25]:
        message = (str(led)+",0,%d,%d")%(int(i*0.2),i)
        serled.write(message+"\n")
        serled.write(str(led)+",0,0,0\n")

# reactions to different events

def reaction(led, duration):
    # reaction to data
    fadeInTurq(led)
    print led, "green"
    time.sleep(duration)
    fadeOutTurq(led)
    # reaction to conversation
    fadeInPurple(led)
    print led, "red"
    time.sleep(duration)
    fadeOutPurple(led)
    #finished

def reaction_sms(number):
    for i in range(number):
        for j in range(4):
            fadeInYellow(j)
        for j in range(4):
            fadeOutYellow(j)


while True: 
    #datas = codecs.open("values-test.txt", "r", encoding="utf-8")
    datas = urllib2.urlopen("http://kucjica.kucjica.org/androidtesting/arduino-get.php")
    line = datas.read()
    #print line

    ### calculate the movement:
    bajts = int(line.split(';')[2])
    print "bajts", bajts
    if 0 <= bajts <= 150:
        speedBajt = 85 #servo up
        sleeping_time = 2
    elif 150 < bajts <= 900:
        speedBajt = 95 # servo down_slow
        sleeping_time = 2
    elif 900 < bajts <= 1600:
        speedBajt = 100 # servo down
        sleeping_time = 1
    elif 1600 < bajts <= 30000:
        speedBajt = 110 # servo down_fast
        sleeping_time = 1
    elif 30000 < bajts:
        speedBajt = 120 # servo down_very_fast
        sleeping_time = 1
    else: 
        print "none of the above byte values"
    conv = int(line.split(';')[3])
    print "conv", conv
    if 0 <= conv <= 2:
        speedConv = 88 #servo up
        sleeping_time = 2
    elif 2 < conv <= 30:
        speedConv = 100 # servo down
        sleeping_time = 1
    elif 30 < conv <= 120:
        speedConv = 110 # servo down_fast
        sleeping_time = 1
    elif 120 < conv:
        speedConv = 120 # servo down_very_fast
        sleeping_time = 1
    else: 
        print "none of the above byte values"
    sms = int(line.split(';')[4])
    print "sms", sms
    if sms >= 1:
        reaction_sms(sms)
    signals = int(line.split(';')[5])
    estimote = line.split(';')[6].strip()
    ### locate in space
    ### and react depending on the closest estimote
    if estimote == "0":
        print "you are not here"
        time.sleep(0.3)
    elif estimote == "62100": #blueberry pie
        print "blueberry"
        print speedBajt
        reaction(1, sleeping_time)
    elif estimote == "56336": #icy marshmallow
        print "icy"
        print speedBajt
        new_speedBajt = int(90-speedBajt)/4 + speedBajt
        new_speedConv = int(90-speedConv)/4 + speedConv
        reaction(2, sleeping_time) # main is gaya
        reaction(1, sleeping_time) # raya is secondary
        # reaction_sec(vlaya, vlayaLED)
    elif estimote == "55745": #mint coctail
        print "mint"
        print speedBajt
        new_speedBajt = int(90-speedBajt)/2 + speedBajt
        new_speedConv = int(90-speedConv)/2 + speedConv
        reaction(3, sleeping_time) # main is vlaya
        reaction(4, sleeping_time) # zlaya is secondary
    else:
        print "estimote weird"                       

    time.sleep(10)
'''
### WORK FLOW:

### read in the db

### parse values; what has changed since last time
####### use timestamp?

### compute the reaction
### lights to represent bytes and conversation

### move things
'''
