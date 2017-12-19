import urllib2, time, glob, serial, random, ledclass

def fadeAll():
    for j in range(4):
        for i in range(255):
            message = ("%d,%d,0,0")%(j,i)
            ledclass.serled.write(message+'\n')
            #time.sleep(0.01)
    for j in range(4):
        for i in range(255):
            message = ("%d,0,%d,0")%(j,i)
            ledclass.serled.write(message+'\n')
            #time.sleep(0.01)
    for j in range(4):
        for i in range(255):       
            message = ("%d,0,0,%d")%(j,i)
            ledclass.serled.write(message+'\n')
            #time.sleep(0.01)

def randomAll():
    for j in range(4):
        red = random.randint(0,255)
        green = random.randint(0,255)
        blue = random.randint(0,255)
        message = ("%d,%d,%d,%d")%(j,red,green,blue)
        ledclass.serled.write(message+'\n')
        time.sleep(0.1)

ledclass.clearAll()
#fadeAll()

while True:
    print "red"
    for i in range(4):
        ledclass.fadeInRed(i)
    time.sleep(3)
    print "green"
    for i in range(4):
        ledclass.fadeInGreen(i)
    time.sleep(3)
    print "turquoise"
    for i in range(4):
        ledclass.fadeInTurq(i)
    time.sleep(3)
    #fadeAll()
