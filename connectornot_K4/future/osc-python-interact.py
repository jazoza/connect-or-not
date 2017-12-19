""" receiving OSC with pyOSC
logs messages received from the android app 'Connect or Not'
(the app sends data on conversation minutes, data packets,
    sms and signalstrength every 10s)
and writes them to a file log+timestamp.csv
https://trac.v2.nl/wiki/pyOSC
adapted example by www.ixi-audio.net based on pyOSC documentation
"""

import OSC, time, threading, codecs
from datetime import datetime
f_out = codecs.open("logs/log"+str(int(time.time()))+".csv", "w", encoding="utf-8")

f_out.write('ID; address; value; timestamp;\n')


# tupple with ip, port. i dont use the ()
# but maybe you want -> send_address = ('127.0.0.1', 9000)
receive_address = '0.0.0.0', 50000


# OSC Server. there are three different types of server.
s = OSC.OSCServer(receive_address) # basic
##s = OSC.ThreadingOSCServer(receive_address) # threading
##s = OSC.ForkingOSCServer(receive_address) # forking


# this registers a 'default' handler (for unmatched messages),
# an /'error' handler, an '/info' handler.
# And, if the client supports it, a '/subscribe' & '/unsubscribe' handler
s.addDefaultHandlers()

veljuz = {'/data':0, '/conversation' : 0, '/sms' : 0, '/signal' : 0, '/celldistance' : 0}
#oldveljuz = {'/data':0, '/conversation' : 0, '/sms' : 0, '/signal' : 0, '/celldistance' : 0}


# define a message-handler function for the server to call.
def all_handler(addr, tags, stuff, source):
    f_out.write(OSC.getUrlStr(source)+'; ')
    #print "(addr : value) %s" % addr, ":", stuff[0]
    f_out.write(addr+'; '+str(stuff[0])+'; '+str(time.time())+'; ')
    f_out.write('humanreadable: '+datetime.fromtimestamp(int(time.time())).strftime('%Y-%m-%d %H:%M:%S'))
    f_out.write('\n')
    global veljuz
    #global oldveljuz
    for i in range(len(veljuz)):
        if addr == veljuz.items()[i][0]:
            # updating key/value pairs
            veljuz[veljuz.items()[i][0]] = stuff[0]
            if stuff[0] != 0:
                if addr == '/conversation':
                    print 'BLINKING FOR', stuff[0], 'SECONDS'
                elif addr == '/data':
                    print 'RAINBOW WITH SPEED', stuff[0]
                elif addr == '/sms':
                    print 'TURN THE CLOSEST LED RED', stuff[0], 'TIMES'
                elif addr == '/signal':
                    print 'FADE BY', stuff[0]
                else:
                    continue

    #print 'vejluz ', veljuz



for i in range(len(veljuz)):
    s.addMsgHandler(veljuz.items()[i][0], all_handler) # adding our function

# just checking which handlers we have added
print "Registered Callback-functions are :"
for addr in s.getOSCAddressSpace():
    print addr


# Start OSCServer
print "\nStarting OSCServer. Use ctrl-C to quit."
st = threading.Thread(target = s.serve_forever)
st.start()

try:
    while 1:
        #print veljuz
        time.sleep(5)

except KeyboardInterrupt:
    print "\nClosing OSCServer."
    s.close()
    print "Waiting for Server-thread to finish"
    st.join() ##!!!
    print "Done"
    f_out.close()
