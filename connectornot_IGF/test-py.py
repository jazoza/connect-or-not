import time, sys

while True:
	try:
		print("running")
		time.sleep(5)
	except KeyboardInterrupt:
		print("exiting")
		sys.exit()
