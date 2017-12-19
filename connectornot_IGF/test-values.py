import time, sys, random # ledclass,
from urllib.request import urlopen
from scipy.interpolate import interp1d

def valuecase(value,scaling):
    s = interp1d([scaling[0], scaling[1]],[89,10])
    t = interp1d([scaling[0], scaling[1]],[1,4])
    if value > scaling[1]:
        speed = 10
        sleeping_time = 4
    else:
        speed = int(s(value))
        sleeping_time = float(t(value))
    return [speed, sleeping_time]

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
        print("bajts", bajts)
        bajtsLimit=[0, 300000]
        speedBajt, sleepBajt = valuecase(bajts, bajtsLimit)
        print("speed according to bytes(which are ", bajts, speedBajt)
        conv = int(line.split(b';')[3])
        print("conv", conv)
        convLimit=[0, 120]
        speedConv, sleepConv = valuecase(conv, convLimit)
        print("speed according to conversation", speedConv)
        sms = int(line.split(b';')[4])
        print("sms", sms)
        smsLimit = [0, 4]
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
        # if fingerprint == "0":
        #     print("you are not here")
        #     breathing(servoList[0], servoList[1], servoList[2], speedFinal, speedFinal, sleepFinal)
        #         #ledclass.fadeInRed(i)
        # elif fingerprint == "131": # ulaz
        #     print('you are at ULAZ')
        #     breathing(servoList[0], servoList[1], servoList[2], speedFinal, speedFinal-2, sleepFinal)
        # elif fingerprint == "132": # izlaz
        #     print('you are at IZlAZ')
        #     breathing(servoList[1], servoList[0], servoList[2], speedFinal, speedFinal-2, sleepFinal)
        # else:
        #     print("something weird")
        #     breathing(servoList[0], servoList[1], servoList[2], speedFinal, speedFinal, sleepFinal)
        time.sleep(2)
    except KeyboardInterrupt:
        for i in range(len(servoList)):
            servoList[i].move(90)
        sys.exit()
