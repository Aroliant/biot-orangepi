from biot import *
import os
import thread
import sys
from time import *

from pyA20.gpio import gpio
from pyA20.gpio import port

ledState = False

led= port.PA8
button = port.PA6

gpio.init()
gpio.setcfg(led, gpio.OUTPUT)
gpio.setcfg(button,gpio.INPUT)
gpio.pullup(button,gpio.PULLUP)



# LED Test
gpio.output(led, 0)
sleep(1)
gpio.output(led,1)
sleep(1)
gpio.output(led, 0)


DEVICE_ID =  ""
DEVICE_TOKEN = "12345"


IoT = BIoT("192.168.100.10",5000,params = { 'token' : DEVICE_TOKEN })

IoT.wait(2)

def light_state_change(status):
	global ledState
	if status == 1:
		gpio.output(led,True)
		print("server led on")
		ledState = True
		sleep(0.5)

	elif status == 0:
		gpio.output(led,False)
		print("server led off")
		ledState = False
		sleep(0.5)
		print(status)


IoT.on_param_change('status',1,light_state_change)

def listenButton():
	buttonPress = False
	global ledState
	
	while True:
		buttonPress = gpio.input(button)
		if buttonPress == False and ledState==False:
			gpio.output(led,True)
			print("led on")
			IoT.setState(1,'status',1)
			ledState = True
			sleep(0.5)
		
		elif buttonPress == False and ledState ==True:
			gpio.output(led,False)
			print("led off")
			IoT.setState(1,'status',0)
			ledState = False
			sleep(0.5)

# Listening to Button Event
try:
	thread.start_new_thread(listenButton,())

except:
	print("error unable to start thread")
	
	

		  
IoT.wait()

