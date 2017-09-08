from biot import *
import os
import sys
from time import *
import thread
from pyA20.gpio import gpio
from pyA20.gpio import port

led = port.PA12

gpio.init()
gpio.setcfg(led, gpio.OUTPUT)

IoT = BIoT("localhost:", 5000)

IoT.wait(2)

SERVER_STATUS = 0


def loop():
	global SERVER_STATUS
	print("Looping : VAL", SERVER_STATUS)
	if (SERVER_STATUS == 1):
		gpio.output(led, 1)
		sleep(0.2)
		gpio.output(led, 0)
		sleep(0.2)
		loop()
	else:
		gpio.output(led, 0)
		sleep(0.6)
		loop()


def lightstatechange(status):
	global SERVER_STATUS

	if status == "1":
		SERVER_STATUS = 1
	else:
		SERVER_STATUS = 0

	print("STATUS CHANGED", status);


IoT.on_param_change('status', '1', lightstatechange)
thread.start_new_thread(loop, ())
IoT.wait()
