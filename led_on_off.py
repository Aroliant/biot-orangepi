from biot import *
import os
import sys
from time import *

from pyA20.gpio import gpio
from pyA20.gpio import port

led = port.PA12

gpio.init()
gpio.setcfg(led, gpio.OUTPUT)

# LED Test
gpio.output(led, 0)
sleep(1)
gpio.output(led, 1)
sleep(1)
gpio.output(led, 0)

DEVICE_ID = ""
DEVICE_TOKEN = "12345"

IoT = BIoT("192.168.100.10", 5000, params={'token': DEVICE_TOKEN})

IoT.wait(2)


def light_state_change(status):
	if status == 0:
		gpio.output(led, 0)
		print("LIGHT OFF")
	else:
		gpio.output(led, 1)
		print("LIGHT ON")
	print(status)


IoT.on_param_change('status', 1, light_state_change)

IoT.wait()
