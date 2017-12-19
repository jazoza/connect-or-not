import serial, glob

try:
    portled = glob.glob("/dev/arduino-leds")[0]
except IndexError:
    portled = glob.glob("/dev/ttyACM0")[0]
print "portled", portled
serled = serial.Serial(portled, 19200, timeout=1)

def clearAll():
    for j in range(4):
        message = ("%d,0,0,0")%(j)
        serled.write(message+'\n')

def fadeIn(led, color):
    for i in range(255)[::15]:
        if color == "red":
            r = i
            g = 0
            b = 0
        elif color == "green":
            r = 0
            g = i
            b = 0
        message = (str(led)+",%d,%d,%d")%(r,g,b)
        serled.write(message+"\n")

def fadeInRed(led):
    for i in range(255)[::15]:
        message = (str(led)+",%d,0,0")%(i)
        serled.write(message+"\n")

def fadeInGreen(led):
    for i in range(255)[::15]:
        message = (str(led)+",0,0,%d")%(i)
        serled.write(message+"\n")

def fadeInYellow(led):
    for i in range(255)[::15]:
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
